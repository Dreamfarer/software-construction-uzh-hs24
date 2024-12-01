# GROUP33 – Software Construction HS24 Task III
**Implement our own version control system called tig**\
*By Ceyhun, Gianluca and Mischa*

## Table of Contents
- [Overview](#overview): Explanation and design decisions
- [Java Translation](#java-translation): Challenges encountered during the Python-to-Java translation
- [Java Installation](#java-installation): Dependency installation and compilation guide
- [Disclaimer](#disclaimer): Use of AI tools and commit distribution
- [Code Documentation](#interpreter-documentation): Comprehensive overview of the Python implementation

## Overview
This section outlines our approach and the rationale behind the key design decisions for the Python implementation. For detailed information about individual classes and methods, please refer to the [Code Documentation](#code-documentation).

### Object-Oriented Design Principles
From the start, we designed the Python implementation of Tig with Java's object-oriented structure in mind. By adhering to strict typing and modular design principles, we ensured the Python code was closely aligned with Java’s paradigms, reducing the complexity of translation.

### Command-Driven Architecture
To enhance modularity, we implemented a class for each major command (e.g., `Backup`, `Commit`, `Stage`). These classes not only execute their respective commands but also provide interfaces for interaction with other components. Supporting classes like `Record` and `Parser`, as well as a general-purpose `Tig` class, complete the architecture.

Below is a high-level description of the key classes:

- **Parser (Helper Class)**
  Processes user commands and routes them to the appropriate classes for execution.

- **Record (Helper Class)**
  Represents entries in the repository's metadata files (e.g., commits and `.status.json`), holding attributes such as filenames, hashes, and statuses (untracked, modified, staged, or committed). 

- **Backup (Command Class)**
  Handles file backups and processes the `checkout` command to restore the repository to a specific commit state.

- **Status (Command Class)**
  Manages the `.status.json` file, which dynamically tracks file states before each command execution. This class serves as an interface for querying and updating file states and also processes the `status` command.

- **Stage (Command Class)**
  Handles the `add` command by instructing `Status` to mark files for inclusion in the next commit.

- **Commit (Command Class)**
  Processes the `commit` command, creates commit files, and uses `Backup` to archive files. It also provides access to commit history for other commands.

- **Tig (General-Purpose Class)**
  Handles lightweight commands like `init`, `log`, and `diff`. It initializes repositories, retrieves commit logs, and computes differences between file states. As the main entry point for Tig, it forwards commands to the `Parser`.

## Java Translation
Our Python implementation’s object-oriented design significantly simplified the transition to Java. However, several challenges specific to Java emerged:

- **Imports and Libraries**
  Python’s standard library includes tools like `difflib`, but Java lacks a direct equivalent. For the `Tig.diff` functionality, we used the [java-diff-utils](https://github.com/java-diff-utils/java-diff-utils) library, which required additional configuration.

- **Error Handling**
  Java’s stricter error-handling requirements demanded careful planning, especially when exceptions needed to propagate through multiple layers of the program. This was more structured than Python’s flexible, on-demand approach to error handling.

- **JSON Handling**
  While Python's native JSON library simplifies serialization, Java lacks a built-in equivalent. To maintain simplicity, we implemented custom JSON parsing logic instead of relying on third-party libraries.

- **AI Usage**
  During the Python-to-Java translation, we used ChatGPT to generate Java code from Python input. While this provided a strong foundation, the generated code required manual corrections and integration with our existing codebase. However, this process deepened our understanding of Java’s syntax and modules.

## Java Installation 

## Disclaimer