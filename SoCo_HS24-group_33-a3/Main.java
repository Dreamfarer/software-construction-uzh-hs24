import java.io.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("No command provided.");
            return;
        }
        Parser.parse(args);
    }
}

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
        TIG.init(directory);
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
        int n = args.length > 1 ? Integer.parseInt(args[1]) : -5;
        TIG.log(n);
    }

    private static void handleDiff(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: diff <filename>");
            return;
        }
        String filename = args[1];
        TIG.diff(filename); 
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
        String absolutePath;
        try {
            absolutePath = file.getCanonicalPath();
        } catch (IOException e) {
            throw new RuntimeException("Error getting canonical path for file: " + filename, e);
        }

        MessageDigest sha1;
        try {
            sha1 = MessageDigest.getInstance("SHA-1");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-1 algorithm not found", e);
        }
        sha1.update(absolutePath.getBytes());

        StringBuilder hexString = new StringBuilder();
        for (byte b : sha1.digest()) {
            hexString.append(String.format("%02x", b));
        }
        return hexString.toString();
    }
}

class Stage {
    public static void add(String filename) {
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
            String recordsJson = jsonString.substring(jsonString.indexOf("\"records\": [") + 11, jsonString.lastIndexOf("]"));
            String[] recordObjects = recordsJson.split("\\},\\{");
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
        String pattern = "\"" + key + "\":\\s*\"([^\"]+)\"";
        return json.replaceAll(pattern, "$1");
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
                Path destinationPath = Paths.get(record.getFilename());
                restoredFiles.add(destinationPath.toString());
                Files.copy(sourcePath, destinationPath, StandardCopyOption.REPLACE_EXISTING);
            } catch (IOException e) {
                throw new RuntimeException("Error restoring file: " + record.getFilename(), e);
            }
        }

        try {
            List<String> untrackedFiles = Status.untracked();
            Path currentDir = Paths.get("").toAbsolutePath();
            Files.walk(currentDir)
                .filter(path -> !Files.isDirectory(path))
                .forEach(filePath -> {
                    try {
                        if (!restoredFiles.contains(filePath.toString()) && !untrackedFiles.contains(filePath.toString())) {
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
