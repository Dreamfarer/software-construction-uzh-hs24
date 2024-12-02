# GROUP33 – Software Construction HS24 Task III

**Implement our own version control system called tig**\
_By Ceyhun, Gianluca and Mischa_

## Table of Contents

- [Overview](#overview): Explanation and design decisions
- [Java Translation](#java-translation): Challenges encountered during the Python-to-Java translation
- [Java Installation](#java-installation): Dependency installation and compilation guide
- [Disclaimer](#disclaimer): Use of AI tools and commit distribution
- [Python Walkthrough](#python-walkthrough): Step-by-step walkthrough with `tig.py` according to the use case outline in the assignment
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

Below are two methods for installing dependencies and compiling the code. Please note that the instructions have been tested only on Windows 11 machines. Adjust accordingly for other operating systems.

### Method 1: Maven (Recommended)

1. Install [Maven](https://maven.apache.org/install.html).
2. Navigate to the root directory of Tig, which contains the `pom.xml` file.
3. Run the following command:
   ```sh
   mvn compile
   ```
4. Use Tig as follows:
   ```sh
   java Tig init repo_java
   cd repo_java
   java ../Tig add file.txt
   ```

### Method 2: Manual Compilation

1. Download the [java-diff-utils-4.15.jar](https://repo1.maven.org/maven2/io/github/java-diff-utils/java-diff-utils/4.15/java-diff-utils-4.15.jar) file.
2. Place it in the root directory alongside the Java source code.
3. Compile Tig using this command:
   ```sh
   javac -cp "java-diff-utils-4.15.jar;." Main.java
   ```
4. Use Tig as follows:
   ```sh
   java -cp "java-diff-utils-4.15.jar;." Tig init repo_java
   cd repo_java
   java -cp "..\java-diff-utils-4.15.jar;.." Tig add file.txt
   ```

## Disclaimer

We aimed to distribute the workload as evenly as possible, and overall, this was successful. However, the commit count varies due to different committing habits. Additionally, [Dreamfarer](https://gitlab.uzh.ch/Dreamfarer) handled most of the merge requests, resulting in a higher number of commits on his part.

ChatGPT was primarily used as a tool for documentation, grammar correction, and debugging guidance. While the AI provided valuable help during the Python-to-Java translation, all core implementations in Python were authored exclusively by the group members. For more details on AI usage in the Java translation, refer to the [Java Translation](#java-translation) section.

## Python Walkthrough

The following Python step-by-step walkthrough closely mirrors the use case outlined in the assignment. The commands remain exactly the same; however, the structure has been slightly adjusted in steps 7, 8, and 9 to ensure there is always an output to show.

### 1. Create a directory and initialize a `tig` repository:

```powershell
mkdir repo
python tig.py init repo
```

### 2. Create two new files in the repository:

```powershell
cd repo
echo "Initial content" > file.txt
echo "Initial content of the other file" > other_file.txt
python ../tig.py status
```

**Output:**

```
Filename       | Status    | Hash
-------------------------------------
file.txt       | untracked | 5818c589
other_file.txt | untracked | a20d8634
```

### 3. Start tracking the files:

```powershell
python ../tig.py add file.txt
python ../tig.py add other_file.txt
python ../tig.py status
```

**Output:**

```
Filename       | Status | Hash
----------------------------------
file.txt       | staged | 5818c589
other_file.txt | staged | a20d8634
```

### 4. Commit the files:

```powershell
python ../tig.py commit "Initial commit"
python ../tig.py status
```

**Output:**

```
Filename       | Status   | Hash
------------------------------------
file.txt       | commited | 5818c589
other_file.txt | commited | a20d8634
```

### 5. Modify one file:

```powershell
echo "Updated content" >> file.txt
python ../tig.py status
```

**Output:**

```
Filename       | Status   | Hash
------------------------------------
file.txt       | modified | 1e72cd81
other_file.txt | commited | a20d8634
```

### 6. Check the difference since the last commit:

```powershell
python ../tig.py diff file.txt
```

**Output:**

```
--- file.txt (old)
+++ file.txt (new)
@@ -1,3 +1,5 @@
 ÿþInitial content



+Updated content

+
```

### 7. Stage and commit the modified file:

```powershell
python ../tig.py add file.txt
python ../tig.py commit "Updated content in file.txt"
python ../tig.py log
```

**Output:**

```
commit f77a5c9b
Date:   2024-12-02 11:39:46

    Initial commit

commit 272fb8d0
Date:   2024-12-02 11:40:38

    Updated content in file.txt
```

### 8. Reset (checkout) the repo to the first commit, making file.txt go back to it’s original content:

```powershell
python ../tig.py checkout f77a5c9b
python ../tig.py status
```

**Output:**

```
Filename       | Status   | Hash
------------------------------------
file.txt       | modified | 5818c589
other_file.txt | commited | a20d8634
```

## Code Documentation

<a id="backup.Backup"></a>

### Backup (backup.py)

```python
class Backup()
```

Handles file backups and processes the `checkout` command to restore the repository to a specific commit state.

<a id="backup.Backup.add"></a>

#### add

```python
@staticmethod
def add(directory: str, records: Record | list[Record]) -> None
```

Add a backup of the provided files to the provided directory.

**Arguments**:

- `directory` _str_ - The target directory where backups will be stored.
- `records` _Record | list[Record]_ - The record(s) of files to be backed up.

**Returns**:

None

<a id="backup.Backup.checkout"></a>

#### checkout

```python
@staticmethod
def checkout(id: str) -> None
```

Restore the working directory to the state of a specific commit.

**Arguments**:

- `id` _str_ - The commit ID to restore to.

**Returns**:

None

<a id="commit.Commit"></a>

### Commit (commit.py)

```python
class Commit()
```

Processes the `commit` command, creates commit files, and uses `Backup` to archive files. It also provides access to commit history for other commands.

<a id="commit.Commit.__init__"></a>

#### \_\_init\_\_

```python
def __init__(date: str,
             message: str,
             records: list[Record],
             commit_id: str = None) -> None
```

Initializes a Commit instance.

**Arguments**:

- `date` _str_ - The date of the commit.
- `message` _str_ - The commit message.
- `records` _list[Record]_ - The records associated with this commit.
- `commit_id` _str, optional_ - The unique identifier for the commit. Defaults to None.

**Returns**:

None

<a id="commit.Commit.commit"></a>

#### commit

```python
@staticmethod
def commit(message: str) -> None
```

Creates a new commit and instructs a status chanage and the creation of a backup for the files in the commit.

**Arguments**:

- `message` _str_ - The commit message.

**Returns**:

None

<a id="commit.Commit.all"></a>

#### all

```python
@staticmethod
def all() -> list["Commit"]
```

Retrieves all commits in chronological order.

**Returns**:

- `list[Commit]` - A list of all commits, sorted from oldest to newest.

<a id="commit.Commit.latest"></a>

#### latest

```python
@staticmethod
def latest() -> "Commit"
```

Retrieves the most recent commit.

**Returns**:

- `Commit` - The latest commit.

<a id="commit.Commit.id"></a>

#### id

```python
def id() -> str
```

Retrieves the unique identifier for this commit.

**Returns**:

- `str` - The commit ID.

<a id="commit.Commit.manifest"></a>

#### manifest

```python
def manifest() -> list[Record]
```

Retrieves all records associated with this commit.

**Returns**:

- `list[Record]` - A list of records associated with this commit.

<a id="commit.Commit.files"></a>

#### files

```python
def files() -> list[str]
```

Retrieves all file names from the records associated with this commit.

**Returns**:

- `list[str]` - A list of names of all files present in the records associated with this commit.

<a id="commit.Commit.write"></a>

#### write

```python
def write() -> "Commit"
```

Writes the commit information to a JSON file. Creates a file named commit_xxx.json containing the commit ID, date, message, and records.

**Returns**:

- `Commit` - The commit itself.

<a id="commit.Commit.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the this commit.

**Returns**:

- `str` - A formatted string containing the commit ID, date, and message of this commit.

<a id="parser.Parser"></a>

### Parser (parser.py)

```python
class Parser()
```

Processes user commands and routes them to the appropriate classes for execution.

<a id="parser.Parser.parse"></a>

#### parse

```python
@staticmethod
def parse() -> None
```

Parses command-line arguments and executes the appropriate functions based on the command.

Commands:

- `init`: Initialize a repository.
- `add`: Add a file to the staged state.
- `commit`: Commit staged files with a message.
- `log`: Display the commit history.
- `status`: Show the status of a file.
- `diff`: Display differences for a file.
- `checkout`: Restore files to a specific commit state.

**Returns**:

None

**Raises**:

- `SystemExit` - Raised if incorrect arguments are provided or if `argparse` terminates.

<a id="record.Record"></a>

### Record (record.py)

```python
class Record()
```

Represents entries in the repository's metadata files (e.g., commits and `.status.json`), holding attributes such as filenames, hashes, and statuses (untracked, modified, staged, or committed).

<a id="record.Record.__init__"></a>

#### \_\_init\_\_

```python
def __init__(filename: str, status: int, hash: str = None) -> None
```

Initializes a Record instance.

**Arguments**:

- `filename` _str_ - The name of the file.
- `status` _int_ - The status of the file (e.g., untracked, modified).
- `hash` _str, optional_ - The hash of the file's content. Defaults to None.

**Returns**:

None

<a id="record.Record.to_dict"></a>

#### to_dict

```python
def to_dict() -> dict
```

Convert the this record to a dictionary.

**Returns**:

- `dict` - A dictionary representation of this record.

<a id="record.Record.to_dicts"></a>

#### to_dicts

```python
@staticmethod
def to_dicts(records: list["Record"])
```

Convert a list of records to a list of dictionaries.

**Arguments**:

- `records` _list[Record]_ - A list of records.

**Returns**:

- `list[dict]` - A list of dictionaries representing the records.

<a id="record.Record.get_hash"></a>

#### get_hash

```python
@staticmethod
def get_hash(filename: str) -> str
```

Get the SHA-1 hash of a specific file in the current working directory. Reads the file in chunks of 4 KB to compute the hash.

**Arguments**:

- `filename` _str_ - The name of the file for which to compute the hash.

**Returns**:

- `str` - The first 8 characters of the computed SHA-1 hash.

<a id="stage.Stage"></a>

### Stage (stage.py)

```python
class Stage()
```

Handles the `add` command by instructing `Status` to mark files for inclusion in the next commit.

<a id="stage.Stage.add"></a>

#### add

```python
@staticmethod
def add(filename: str) -> None
```

Instructing 'Status' to add the file to the '.status.json' staging area.

**Arguments**:

- `filename` _str_ - The name of the file to be staged.

**Returns**:

None

<a id="status.Status"></a>

### Status (status.py)

```python
class Status()
```

Manages the `.status.json` file, which dynamically tracks file states before each command execution. This class serves as an interface for querying and updating file states and also processes the `status` command.

<a id="status.Status.untracked"></a>

#### untracked

```python
@staticmethod
def untracked() -> list[Record]
```

Retrieves all untracked records.

**Returns**:

- `list[Record]` - A list of untracked records.

<a id="status.Status.modified"></a>

#### modified

```python
@staticmethod
def modified() -> list[Record]
```

Retrieves all modified records.

**Returns**:

- `list[Record]` - A list of modified records.

<a id="status.Status.staged"></a>

#### staged

```python
@staticmethod
def staged() -> list[Record]
```

Retrieves all staged records.

**Returns**:

- `list[Record]` - A list of staged records.

<a id="status.Status.commited"></a>

#### commited

```python
@staticmethod
def commited() -> list[Record]
```

Retrieves all committed records.

**Returns**:

- `list[Record]` - A list of committed records.

<a id="status.Status.all"></a>

#### all

```python
@staticmethod
def all() -> list[Record]
```

Retrieves all records.

**Returns**:

- `list[Record]` - A list of all records.

<a id="status.Status.add"></a>

#### add

```python
@staticmethod
def add(record: Record) -> None
```

Add a new record to the '.status.json' file. If the record already exists (same filename or same hash), merely modify it without adding.

**Arguments**:

- `record` _Record_ - The record to be added.

**Returns**:

None

<a id="status.Status.remove"></a>

#### remove

```python
@staticmethod
def remove(record: Record) -> None
```

Remove a specific record from the '.status.json' file. Identifies the record by matching the filename and hash.

**Arguments**:

- `record` _Record_ - The record to be removed.

**Returns**:

None

<a id="status.Status.move"></a>

#### move

```python
@staticmethod
def move(record: Record, hash: str, status: int) -> None
```

Move a record into another status (e.g., go from staged to committed).

**Arguments**:

- `record` _Record_ - The record to move.
- `hash` _str_ - The new hash for the record.
- `status` _int_ - The new status to assign to the record.

**Returns**:

None

<a id="status.Status.status"></a>

#### status

```python
@staticmethod
def status() -> None
```

Print the current status of each file in the working directory, indicating if they are untracked, modified, staged, or committed.

**Returns**:

None

<a id="status.Status.sync"></a>

#### sync

```python
@staticmethod
def sync() -> None
```

Synchronize the current files in the working directory with the '.status.json' file.
If the filename or hash of a file has changed, update its status accordingly.

**Returns**:

None

<a id="tig.TIG"></a>

### TIG (tig.py)

```python
class TIG()
```

Handles lightweight commands like `init`, `log`, and `diff`. It initializes repositories, retrieves commit logs, and computes differences between file states. As the main entry point for Tig, it forwards commands to the `Parser`.

<a id="tig.TIG.init"></a>

#### init

```python
@staticmethod
def init(dir: str) -> None
```

Creates a new '.tig/' folder inside the provided path.

**Arguments**:

- `dir` _str_ - The directory in which to create the '.tig/' folder.

**Returns**:

None

<a id="tig.TIG.log"></a>

#### log

```python
@staticmethod
def log(number: int) -> None
```

Prints the commit ID, commit date, and commit message of the last N commits. If `number` is not provided, defaults to N=5.

**Arguments**:

- `number` _int_ - The number of recent commits to display.

**Returns**:

None

<a id="tig.TIG.diff"></a>

#### diff

```python
@staticmethod
def diff(filename: str) -> None
```

Compares the current version of a file with its last committed version. Prints the differences in a unified diff format.

**Arguments**:

- `filename` _str_ - The name of the file to compare.

**Returns**:

None

**Raises**:

- `FileNotFoundError` - If the specified file does not exist.
- `ValueError` - If the file is not found in the repository's status or commits.

<a id="tig.TIG.is_repository"></a>

#### is_repository

```python
@staticmethod
def is_repository() -> bool
```

Checks if the current working directory is a TIG repository.

**Returns**:

- `bool` - True if the current working directory is a TIG repository, False otherwise.
