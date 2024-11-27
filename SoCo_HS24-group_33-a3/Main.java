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