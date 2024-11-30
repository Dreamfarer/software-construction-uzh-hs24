import java.io.*;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;
import com.github.difflib.DiffUtils;
import com.github.difflib.patch.Patch;



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