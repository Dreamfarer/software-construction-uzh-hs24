import java.io.*;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import com.github.difflib.DiffUtils;
import com.github.difflib.patch.Patch;


class Parser {
    public static void parse(String[] args) {
        if (args.length == 0) {
            printHelp();
            return;
        }

        String command = args[0];

        switch (command) {
            case "status":
                handleStatus();
                break;
            case "init":
                handleInit(args);
                break;
            case "add":
                handleAdd(args);
                break;
            case "commit":
                handleCommit(args);
                break;
            case "log":
                handleLog(args);
                break;
            case "diff":
                handleDiff(args);
                break;
            case "checkout":
                handleCheckout(args);
                break;
            default:
                System.out.println("Unknown command: " + command);
                printHelp();
                break;
        }
    }

    private static void handleStatus() {
        Status.status();
    }

    private static void handleInit(String[] args) {
        String directory = args.length > 1 ? args[1] : ".";
        Tig.init(directory);
    }

    private static void handleAdd(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: add <filename>");
            return;
        }
        String filename = args[1];
        Stage.add(filename);
    }

    private static void handleCommit(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: commit <message>");
            return;
        }
        String commitMessage = args[1];
        Commit.commit(commitMessage);
    }

    private static void handleLog(String[] args) {
        int n = args.length > 1 ? Integer.parseInt(args[1]) : 5;
        Tig.log(n);
    }

    private static void handleDiff(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: diff <filename>");
            return;
        }
        String filename = args[1];
        Tig.diff(filename); 
    }

    private static void handleCheckout(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: checkout <commit_id>");
            return;
        }
        String commitId = args[1];
        Backup.checkout(commitId);
    }

    private static void printHelp() {
        System.out.println("Usage:");
        System.out.println("  init [directory]      Initialize a new repository");
        System.out.println("  add <filename>        Add a file to the staging area");
        System.out.println("  commit <message>      Commit changes with a message");
        System.out.println("  log [N]               Show the last N commits (default is 5)");
        System.out.println("  status                Show the current status of files");
        System.out.println("  diff <filename>       Show differences for a file");
        System.out.println("  checkout <commit_id>  Restore files to a specific commit state");
    }
}

class Record {
    public static final int UNTRACKED = 0;
    public static final int MODIFIED = 1;
    public static final int STAGED = 2;
    public static final int COMMITTED = 3;
    public static final String[] REPRESENT = {"untracked", "modified", "staged", "committed"};

    private String filename;
    private int status;
    private String hash;

    public Record(String filename, int status) {
        this(filename, status, null);
    }

    public Record(String filename, int status, String hash) {
        this.filename = filename;
        this.status = status;
        this.hash = hash != null ? hash : getHash(filename);
    }

    public String getFilename() {
        return filename;
    }

    public int getStatus() {
        return status;
    }

    public String getHash() {
        return hash;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }

    public java.util.Map<String, Object> toDict() {
        java.util.Map<String, Object> recordMap = new java.util.HashMap<>();
        recordMap.put("filename", this.filename);
        recordMap.put("hash", this.hash);
        recordMap.put("status", this.status);
        return recordMap;
    }

    public static List<java.util.Map<String, Object>> toDicts(List<Record> records) {
        List<java.util.Map<String, Object>> dicts = new ArrayList<>();
        for (Record record : records) {
            dicts.add(record.toDict());
        }
        return dicts;
    }
    public static String getHash(String filename) {
        File file = new File(filename);
        MessageDigest sha1;
        try {
            sha1 = MessageDigest.getInstance("SHA-1");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-1 algorithm not found", e);
        }
        try (InputStream fis = new FileInputStream(file)) {
            byte[] buffer = new byte[1024];
            int read;
            while ((read = fis.read(buffer)) != -1) {
                sha1.update(buffer, 0, read);
            }
        } catch (IOException e) {
            throw new RuntimeException("Error reading file for hashing: " + filename, e);
        }
        StringBuilder hexString = new StringBuilder();
        for (byte b : sha1.digest()) {
            hexString.append(String.format("%02x", b));
        }
        return hexString.toString();
    }
}

class Stage {
    public static void add(String filename) {
        if (Status.IsIgnored(filename)) {
            System.out.println("File " + filename + " is ignored and can't be staged.");
        }
        Status.add(new Record(filename, Record.STAGED));
    }
}

class Commit {
    private String id;
    private String date;
    private String message;
    private List<Record> manifest;

    public Commit(String date, String message, List<Record> records, String commitId) {
        this.date = date;
        this.message = message;
        this.manifest = records;
        this.id = (commitId != null) ? commitId : generateUniqueId();
    }

    public static void commit(String message) {
        List<Record> stagedFiles = Status.staged();
        if (stagedFiles.isEmpty()) {
            System.out.println("No changes to commit.");
            return;
        }

        String commitDate = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        Commit newCommit = new Commit(commitDate, message, stagedFiles, null);

        for (Record record : stagedFiles) {
            Status.move(record, record.getHash(), Record.COMMITTED);
        }

        newCommit.write();
        Backup.add(".tig/backup", stagedFiles);
    }

    public static List<Commit> all() {
        List<Commit> commits = new ArrayList<>();
        File commitFolder = new File(".tig/commits");
        if (!commitFolder.exists() || !commitFolder.isDirectory()) {
            return commits;
        }

        File[] commitFiles = commitFolder.listFiles((_, name) -> name.startsWith("commit_"));
        if (commitFiles == null) {
            return commits;
        }

        for (File file : commitFiles) {
            commits.add(read(file));
        }
        return commits;
    }

    public static Commit latest() {
        List<Commit> commits = all();
        return commits.isEmpty() ? null : commits.get(commits.size() - 1);
    }

    public String getId() {
        return id;
    }

    public String getDate() {
        return date;
    }

    public String getMessage() {
        return message;
    }

    public List<Record> manifest() {
        return manifest;
    }

    public List<String> files() {
        List<String> filenames = new ArrayList<>();
        for (Record record : manifest) {
            filenames.add(record.getFilename());
        }
        return filenames;
    }

    public void write() {
        String commitFilename = String.format(".tig/commits/commit_%s_%s.json", id,
                date.replace(" ", "_").replace(":", "-"));
        File commitFile = new File(commitFilename);
        commitFile.getParentFile().mkdirs();

        try (FileWriter writer = new FileWriter(commitFile)) {
            StringBuilder json = new StringBuilder();
            json.append("{\n");
            json.append("\"commit_id\": \"").append(id).append("\",\n");
            json.append("\"date\": \"").append(date).append("\",\n");
            json.append("\"message\": \"").append(message).append("\",\n");
            json.append("\"records\": [\n");
            for (int i = 0; i < manifest.size(); i++) {
                Record record = manifest.get(i);
                json.append("  {\n");
                json.append("    \"filename\": \"").append(record.getFilename()).append("\",\n");
                json.append("    \"status\": ").append(record.getStatus()).append(",\n");
                json.append("    \"hash\": \"").append(record.getHash()).append("\"\n");
                json.append("  }");
                if (i < manifest.size() - 1) {
                    json.append(",");
                }
                json.append("\n");
            }
            json.append("]\n");
            json.append("}\n");

            writer.write(json.toString());
        } catch (IOException e) {
            throw new RuntimeException("Error writing commit file: " + commitFilename, e);
        }
    }

    private String generateUniqueId() {
        String data = message + date;
        try {
            MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
            byte[] hash = sha256.digest(data.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                hexString.append(String.format("%02x", b));
            }
            return hexString.substring(0, 8);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not found", e);
        }
    }

    private static Commit read(File file) {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            StringBuilder json = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                json.append(line.trim());
            }

            String jsonString = json.toString();
            String id = extractValue(jsonString, "commit_id");
            String date = extractValue(jsonString, "date");
            String message = extractValue(jsonString, "message");

            List<Record> records = new ArrayList<>();
            String recordsJson = jsonString.substring(jsonString.indexOf("\"records\": [") + 11, jsonString.lastIndexOf("]") + 1);
            if (recordsJson.trim().isEmpty()) {
                throw new IllegalStateException("No records found in JSON");
            }
            String[] recordObjects = recordsJson.split("(?<=\\}),\\s*(?=\\{)");
            for (String recordJson : recordObjects) {
                String filename = extractValue(recordJson, "filename");
                int status = Integer.parseInt(extractValue(recordJson, "status"));
                String hash = extractValue(recordJson, "hash");
                records.add(new Record(filename, status, hash));
            }

            return new Commit(date, message, records, id);
        } catch (IOException e) {
            throw new RuntimeException("Error reading commit file: " + file.getAbsolutePath(), e);
        }
    }

    private static String extractValue(String json, String key) {
        String pattern = "\"" + key + "\"\\s*:\\s*\"?([^\"]+?)\"?\\s*(,|})";
        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(json);
        if (matcher.find()) {
            return matcher.group(1).trim();
        } else {
            throw new IllegalArgumentException("Key " + key + " not found in JSON: " + json);
        }
    }


    @Override
    public String toString() {
        return String.format("\033[33mcommit %s\033[0m\nDate: %s\n\n   %s\n", id, date, message);
    }
}

class Backup {
    public static void add(String directory, Object records) {
        List<Record> recordList = new ArrayList<>();
        if (records instanceof Record) {
            recordList.add((Record) records);
        } else if (records instanceof List<?>) {
            for (Object obj : (List<?>) records) {
                if (obj instanceof Record) {
                    recordList.add((Record) obj);
                }
            }
        }

        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        for (Record record : recordList) {
            try {
                String fileExtension = getFileExtension(record.getFilename());
                String newFilename = record.getHash() + fileExtension;
                Path destinationPath = Paths.get(directory, newFilename);
                Files.copy(Paths.get(record.getFilename()), destinationPath, StandardCopyOption.REPLACE_EXISTING);
            } catch (IOException e) {
                throw new RuntimeException("Error copying file: " + record.getFilename(), e);
            }
        }
    }

    public static void checkout(String id) {
        Commit commit = null;
        for (Commit c : Commit.all()) {
            if (c.getId().equals(id)) {
                commit = c;
                break;
            }
        }

        if (commit == null) {
            System.out.println("No commit found with ID: " + id);
            return;
        }

        List<String> restoredFiles = new ArrayList<>();
        for (Record record : commit.manifest()) {
            try {
                String fileExtension = getFileExtension(record.getFilename());
                Path sourcePath = Paths.get(".tig", "backup", record.getHash() + fileExtension);
                Path destinationPath = Paths.get(record.getFilename()).toAbsolutePath();
                restoredFiles.add(destinationPath.toString());
                Files.copy(sourcePath, destinationPath, StandardCopyOption.REPLACE_EXISTING);
            } catch (IOException e) {
                throw new RuntimeException("Error restoring file: " + record.getFilename(), e);
            }
        }

        try {
            List<Record> untrackedFiles = Status.untracked();
            Set<String> untrackedFilePaths = untrackedFiles.stream()
                    .map(r -> Paths.get(r.getFilename()).toAbsolutePath().toString())
                    .collect(Collectors.toSet());
            Path currentDir = Paths.get("").toAbsolutePath();
            Files.walk(currentDir)
                .filter(path -> !Files.isDirectory(path))
                .filter(path -> !path.startsWith(currentDir.resolve(".tig")))
                .forEach(filePath -> {
                    try {
                        String absoluteFilePath = filePath.toAbsolutePath().toString();
                        if (!restoredFiles.contains(absoluteFilePath) && !untrackedFilePaths.contains(absoluteFilePath)) {
                            Files.delete(filePath);
                        }
                    } catch (IOException e) {
                        throw new RuntimeException("Error deleting file: " + filePath, e);
                    }
                });
        } catch (IOException e) {
            throw new RuntimeException("Error cleaning up untracked files", e);
        }
    }

    private static String getFileExtension(String filename) {
        int index = filename.lastIndexOf('.');
        return index == -1 ? "" : filename.substring(index);
    }
}

class Status {
    public static final Path STATUS_FILE = Paths.get(".tig", ".status.json");
    private static final Path TIGIGNORE_FILE = Paths.get(".tig", ".tigignore");
    private static Set<String> ignoredFiles;

    public static boolean IsIgnored(String filename) {
        if (ignoredFiles == null) {
            loadIgnoredFiles();
        }
        return ignoredFiles.contains(filename);
    }

    private static void loadIgnoredFiles() {
        ignoredFiles = new HashSet<>();
        if (Files.exists(TIGIGNORE_FILE)) {
            try {
                ignoredFiles.addAll(Files.readAllLines(TIGIGNORE_FILE).stream().map(String::trim).collect(Collectors.toSet()));
            } catch (IOException e) {
            }
        }
    }

    public static List<Record> untracked() {
        return readJson().stream().filter(record -> record.getStatus() == Record.UNTRACKED).collect(Collectors.toList());
    }

    public static List<Record> modified() {
        return readJson().stream().filter(record -> record.getStatus() == Record.MODIFIED).collect(Collectors.toList());
    }

    public static List<Record> staged() {
        return readJson().stream().filter(record -> record.getStatus() == Record.STAGED).collect(Collectors.toList());
    }

    public static List<Record> commited() {
        return readJson().stream().filter(record -> record.getStatus() == Record.COMMITTED).collect(Collectors.toList());
    }

    public static List<Record> all() {
        return Status.readJson();
    }

    public static void add(Record record) {
        List<Record> records = Status.readJson();
        for (int i = 0; i < records.size(); i++) {
            Record r = records.get(i);
            if (r.getFilename().equals(record.getFilename()) || r. getHash().equals(record.getHash())) {
                records.set(i, record);
                Status.writeJson(records);
                return;
            }
        }
        records.add(record);
        Status.writeJson(records);
    }

    public static void remove(Record record) {
        List<Record> records = Status.readJson();
        records = records.stream().filter(r -> !(r.getFilename().equals(record.getFilename()) && r.getHash().equals(record.getHash()))).collect(Collectors.toList());
        Status.writeJson(records);
    }

    public static void move(Record record, String hash, int status) {
        List<Record> records = Status.readJson();
        boolean found = false;
        for (Record r : records) {
            if (r.getFilename().equals(record.getFilename()) && r.getHash().equals(record.getHash())) {
                r.setStatus(status);
                r.setHash(hash);
                found = true;
                break;
            }
        }
        if(!found) {
            record.setStatus(status);
            records.add(record);
        }
        writeJson(records);
    }

    public static void status() {
        sync();
        List<Record> records = readJson();
    
        int defaultMinWidth = 10;
        int maxFilenameLength = records.stream().mapToInt(r -> r.getFilename().length()).max().orElse(defaultMinWidth);
        int maxStatusLength = records.stream().mapToInt(r -> Record.REPRESENT[r.getStatus()].length()).max().orElse(defaultMinWidth);
        int maxHashLength = records.stream().mapToInt(r -> r.getHash().length()).max().orElse(defaultMinWidth);
    
        System.out.printf("%-" + maxFilenameLength + "s | %-" + maxStatusLength + "s | %-" + maxHashLength + "s%n", "Filename", "Status", "Hash");
        System.out.println("-".repeat(maxFilenameLength + maxStatusLength + maxHashLength + 6));

        for (Record record : records) {
            System.out.printf("%-" + maxFilenameLength + "s | %-" + maxStatusLength + "s | %-" + maxHashLength + "s%n", record.getFilename(), Record.REPRESENT[record.getStatus()], record.getHash());
        }
    }

    public static void sync() {
        List<Record> currentRecords = all();
        List<Record> currentFiles = records();
        Map<String, Record> filenameLookup = currentRecords.stream().collect(Collectors.toMap(Record::getFilename, r -> r, (_,b) -> b));
        Map<String, Record> hash_lookup = currentRecords.stream().collect(Collectors.toMap(Record::getHash, r -> r, (_,b) -> b));

        for (Record fileRecord : currentFiles) {
            Record existingRecord = filenameLookup.get(fileRecord.getFilename());
            if (existingRecord != null) {
                if (!existingRecord.getHash().equals(fileRecord.getHash())) {
                    move(existingRecord, fileRecord.getHash(), Record.MODIFIED);
                }
            } else {
                Record existingByHash = hash_lookup.get(fileRecord.getHash());
                if (existingByHash != null) {
                    move(existingByHash, fileRecord.getHash(), Record.MODIFIED);
                } else {
                    add(fileRecord);
                }
            }
        }
        Set<String> currentFileNames = currentFiles.stream().map(Record::getFilename).collect(Collectors.toSet());
        for (Record record : currentRecords) {
            if (!currentFileNames.contains(record.getFilename()) && currentFiles.stream().noneMatch(r -> r.getHash().equals(record.getHash()))) {
                remove(record);
            }
        }
    }

    private static List<Record> readJson() {
        List<Record> records = new ArrayList<>();
        if (Files.exists(STATUS_FILE)) {
            File statusFile = STATUS_FILE.toFile();
            try (BufferedReader reader = new BufferedReader(new FileReader(statusFile))) {
                StringBuilder json = new StringBuilder();
                String line;
                while((line = reader.readLine()) != null) {
                    json.append(line.trim());
                }
                String jsonString = json.toString();
                String recordsJson = jsonString.substring(jsonString.indexOf("[") + 1, jsonString.lastIndexOf("]"));
                String[] recordObjects = recordsJson.split("(?<=\\}),(?=\\{)");

                for (String recordJson : recordObjects) {
                    String filename = extractValue(recordJson, "filename");
                    int status = Integer.parseInt(extractValue(recordJson, "status"));
                    String hash = extractValue(recordJson, "hash");
                    records.add(new Record(filename, status, hash));
                }
            } catch (IOException e) {
                throw new RuntimeException("Error reading JSON file: " + statusFile.getAbsolutePath(), e);
            }
        }
        return records;
    }
    
    public static void writeJson(List<Record> records) {
        File statusFile = STATUS_FILE.toFile();
        statusFile.getParentFile().mkdirs();
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(statusFile))) {
            writer.write("[\n");
            for (int i = 0; i < records.size(); i++) {
                Record record = records.get(i);
                String recordJson = String.format("{\"filename\":\"%s\",\"status\":%d,\"hash\":\"%s\"}", record.getFilename(), record.getStatus(), record.getHash());
                writer.write(" " + recordJson);
                if (i < records.size() -1) {
                    writer.write(",\n");
                } else {
                    writer.write("\n");
                }
            }
            writer.write("]");

        } catch (IOException e) {
            throw new RuntimeException("Error writing JSON file: " + statusFile, e);
        }
    }

    private static String extractValue(String json, String key) {
        String pattern = "\"" + key + "\":\"?([^\"]+?)\"?(,|})";
        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(json);
        if (matcher.find()) {
            return matcher.group(1).trim();
        } else {
            throw new IllegalArgumentException("Key " + key + " not found in JSON: " + json);
        }
    }

    @SuppressWarnings("CallToPrintStackTrace")
    private static List<Record> records() {
        List<Record> records = new ArrayList<>();
        try {
            Files.walk(Paths.get(".")).filter(Files::isRegularFile).filter(path -> !path.toString().contains(".tig")).filter(path -> !IsIgnored(path.toString())).forEach(path -> {
                String relativePath = Paths.get(".").relativize(path).toString();
                records.add(new Record(relativePath, Record.UNTRACKED));
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
        return records;
    }
}

class Tig {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("No command provided.");
            return;
        }
        Parser.parse(args);
    }
    @SuppressWarnings("CallToPrintStackTrace")
    public static void init(String dir) {
        Path path = Paths.get(dir, ".tig");
        if (!Files.exists(path)) {
            try {
                Files.createDirectories(path);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public static void log(int number) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        List<Commit> commits = Commit.all().stream()
            .sorted(Comparator.comparing(commit -> LocalDateTime.parse(commit.getDate(), formatter)))
            .collect(Collectors.toList());
    
        int totalCommits = commits.size();
        int start = Math.max(0, totalCommits - number);
    
        for (int i = start; i < totalCommits; i++) {
            Commit commit = commits.get(i);
            System.out.println("commit " + commit.getId());
            System.out.println("Date:    " + commit.getDate());
            System.out.println("\n     " + commit.getMessage() + "\n");
        }
    }

    @SuppressWarnings("CallToPrintStackTrace")
    public static void diff(String filename) {
        Path workingDir = Paths.get(System.getProperty("user.dir"));
        Path filePath = workingDir.resolve(filename);

        if (!Files.exists(filePath)) {
            System.out.println("File: " + filename + " does not exist");
            return;
        }
        String statusFileHash = null;
        Status.sync();
        List<Record> statusRecords = Status.all();

        for (Record record : statusRecords) {
            if (record.getFilename().equals(filename)) {
                statusFileHash = record.getHash();
                break;
            }
        }
        if (statusFileHash == null) {
            System.out.println("File " + filename + " was not found in the current working directory.");
            return;
        }
        List<Commit> allCommits = Commit.all();
        String commitFileHash = null;

        for (Commit commit : allCommits) {
            for (Record record : commit.manifest()) {
                if (record.getFilename().equals(filename)) {
                    commitFileHash = record.getHash();
                    break;
                }
            }
        }
        if (commitFileHash == null) {
            System.out.println("No commit with " + filename + " was not found to perform a diff.");
            return;
        }

        String fileExtension = getFileExtension(filename);
        Path pathOfNewestFile = workingDir.resolve(filename);
        Path pathOfSecondFile = workingDir.resolve(".tig/backup").resolve(commitFileHash + fileExtension);

        try (BufferedReader newFileReader = Files.newBufferedReader(pathOfNewestFile);
             BufferedReader oldFileReader = Files.newBufferedReader(pathOfSecondFile)) {

            List<String> newFileLines = newFileReader.lines().collect(Collectors.toList());
            List<String> oldFileLines = oldFileReader.lines().collect(Collectors.toList());
            
            Patch<String> patch = DiffUtils.diff(oldFileLines,newFileLines);
            patch.getDeltas().forEach(System.out::println);


        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static boolean isRepository() {
        Path repoPath = Paths.get(System.getProperty("user.dir"), ".tig");
        return Files.isDirectory(repoPath);
    }

    private static String getFileExtension(String filename) {
        int dotIndex = filename.lastIndexOf('.');
        return (dotIndex == -1) ? "" : filename.substring(dotIndex);
    }
}