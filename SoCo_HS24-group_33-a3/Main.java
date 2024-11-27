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
