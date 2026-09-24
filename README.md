# Duplicate File Removal Automation

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![Automation](https://img.shields.io/badge/Automation-File%20Management-green)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A Python-based automation tool that recursively scans directories, detects duplicate files using MD5 checksums, removes duplicate copies, generates execution logs, and sends log reports through email.

---

## Project Status

**Completed** ✅

The current version supports:

- Duplicate-file detection
- Automatic duplicate removal
- MD5 checksum comparison
- Recursive directory scanning
- Scheduled execution
- Execution logging
- Email reporting
- Command-line argument validation
- Error and permission handling
- Environment-variable based email configuration

---

## Overview

Duplicate files can unnecessarily consume storage space and make file management difficult.

This project automates the process of finding and removing duplicate files from a specified directory.

Instead of manually searching through folders, the program:

1. Scans the selected directory and its subdirectories.
2. Calculates MD5 checksums for files.
3. Groups files with identical checksums.
4. Retains the first occurrence of a file.
5. Removes subsequent duplicate copies.
6. Generates an execution log.
7. Sends the log through email.
8. Repeats the process automatically according to the configured interval.

---

## Features

- 🔍 Recursively scans directories and subdirectories
- #️⃣ Uses MD5 checksums to identify duplicate files
- 🗑️ Automatically removes duplicate files
- ⏱️ Supports scheduled/interval-based execution
- 📝 Generates detailed execution logs
- 📧 Sends execution reports through email
- 🛡️ Uses environment variables for email credentials
- ⚠️ Handles file and permission-related errors
- 💻 Provides command-line help and usage options
- 🔧 Validates directory, interval, and email inputs

---

## Screenshots

### Terminal Execution

![Terminal Execution](screenshots/Terminal%20execution.png)

### Email Report

![Email Report](screenshots/Email.png)

### Execution Log

![Log File](screenshots/Log%20File.png)

---

## How It Works

The application follows this workflow:

```text
User Input
    │
    ▼
Directory Validation
    │
    ▼
Recursive File Scanning
    │
    ▼
MD5 Checksum Generation
    │
    ▼
Duplicate Detection
    │
    ▼
Duplicate Removal
    │
    ▼
Execution Log Generation
    │
    ▼
Email Report
    │
    ▼
Wait for Configured Interval
    │
    └──────────────► Repeat
```

### Duplicate Detection Logic

The program calculates an MD5 checksum for each file.

If two or more files produce the same checksum, they are treated as duplicates.

The first occurrence is retained and subsequent duplicate copies are removed.

> **Note:** MD5 is used here for file-duplicate detection, not for password or security-sensitive cryptographic purposes.

---

## Technologies Used

- **Python**
- **os**
- **sys**
- **hashlib**
- **datetime**
- **smtplib**
- **email**
- **schedule**

---

## Project Structure

```text
DuplicateFileRemoval/
│
├── duplicate_file_remover.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── .gitattributes
│
└── screenshots/
    ├── Terminal execution.png
    ├── Email.png
    └── Log File.png
```

---

# Installation

## Prerequisites

Before running the project, make sure you have:

- Python 3.x installed
- Git installed
- A Gmail account if email reporting is required

Check your Python installation:

```bash
python --version
```

Check Git:

```bash
git --version
```

---

## Clone the Repository

Clone the repository using:

```bash
git clone https://github.com/bemo-codes/DuplicateFileRemoval.git
```

Navigate into the project:

```bash
cd DuplicateFileRemoval
```

---

## Install Dependencies

Install the required Python package:

```bash
pip install -r requirements.txt
```

The current `requirements.txt` contains:

```text
schedule
```

---

# Environment Configuration

The email functionality uses environment variables so that credentials are not hardcoded into the Python source code.

## 1. Create a `.env` file

Create a file named:

```text
.env
```

Add:

```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

Replace the placeholder values with your own credentials.

### Important

**Never commit `.env` to GitHub.**

The project already includes `.env` in `.gitignore`.

The repository also provides `.env.example` as a safe configuration template.

---

## Gmail App Password

If you are using Gmail for email reporting, use a **Gmail App Password** rather than your normal Gmail password.

Your App Password should never be:

- Written directly inside the Python source code
- Added to `README.md`
- Added to `.env.example`
- Committed to Git
- Shared publicly

---

# Usage

Run the program using:

```bash
python duplicate_file_remover.py <DirectoryPath> <IntervalInMinutes> <ReceiverEmail>
```

### Arguments

| Argument | Description |
|---|---|
| `DirectoryPath` | Directory that should be scanned |
| `IntervalInMinutes` | Time interval between automated scans |
| `ReceiverEmail` | Email address that receives the execution report |

---

## Example

Windows:

```bash
python duplicate_file_remover.py "C:\Users\YourName\Documents\Test" 60 example@gmail.com
```

The above command:

- Scans the specified directory
- Runs every 60 minutes
- Removes detected duplicate files
- Generates a log
- Sends the report to the specified email address

---

# Command-Line Options

## Display Help

```bash
python duplicate_file_remover.py --help
```

Short form:

```bash
python duplicate_file_remover.py -h
```

---

## Display Usage Information

```bash
python duplicate_file_remover.py --usage
```

Short form:

```bash
python duplicate_file_remover.py -u
```

---

# Output

After execution, the program can produce:

### Execution Logs

The application records information about the duplicate-removal operation, including detected files and processing results.

### Email Reports

The generated execution information can be sent to the configured recipient through email.

### Console Output

The program provides information about:

- Directory validation
- Interval validation
- Email validation
- Duplicate detection
- Scheduled execution
- Configuration errors

---

# Error Handling

The application performs validation before starting the scheduled operation.

It handles situations such as:

- Invalid directory paths
- Invalid execution intervals
- Invalid email input
- Missing Gmail environment variables
- File access problems
- Permission-related errors
- Email authentication failures
- Invalid command-line arguments

---

# Security

This project follows basic credential-management practices.

### Credentials are not hardcoded

Email credentials are retrieved from environment variables:

```python
os.environ.get("GMAIL_USER")
os.environ.get("GMAIL_APP_PASSWORD")
```

### `.env` is ignored

The `.gitignore` file prevents `.env` from being committed.

### `.env.example` is safe

The example file contains placeholders rather than real credentials.

Example:

```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

**Never commit real credentials to GitHub.**

---

# Safety Considerations

This program permanently removes files identified as duplicates.

Before running it on an important directory:

- Create a backup of important files.
- Test the program on a sample directory first.
- Verify that the detected duplicates are actually safe to remove.
- Avoid running it against system-critical directories.

The safest way to experiment with the project is to create a dedicated test directory containing copies of files.

---

# Limitations

The current version has a few limitations:

- Duplicate detection is based on MD5 checksums.
- Duplicate files are removed automatically.
- There is currently no `--dry-run` mode.
- Email reporting requires Gmail credentials/App Password configuration.
- The application is command-line based and does not currently provide a graphical interface.

---

# Future Improvements

Planned or possible improvements include:

- [ ] Add `--dry-run` mode
- [ ] Add automated unit tests
- [ ] Add GitHub Actions CI
- [ ] Add SHA-256 checksum support
- [ ] Improve duplicate-selection logic
- [ ] Add a graphical user interface
- [ ] Add configurable logging levels
- [ ] Add support for additional email providers
- [ ] Add configuration through a dedicated configuration file
- [ ] Improve reporting with duplicate statistics and storage savings

---

# Testing

The project has been manually tested for:

- Directory validation
- Time-interval validation
- Email validation
- Command-line argument handling
- `--help` option
- `--usage` option
- Duplicate-file detection
- Duplicate-file removal
- Log generation
- Environment-variable based email configuration

Python syntax can be checked using:

```bash
python -m py_compile duplicate_file_remover.py
```

---

# Example Workflow

A typical workflow looks like this:

```text
1. Clone repository
        │
        ▼
2. Install dependencies
        │
        ▼
3. Configure environment variables
        │
        ▼
4. Select directory to scan
        │
        ▼
5. Run duplicate_file_remover.py
        │
        ▼
6. Files are scanned recursively
        │
        ▼
7. MD5 checksums are calculated
        │
        ▼
8. Duplicate files are identified
        │
        ▼
9. Duplicate copies are removed
        │
        ▼
10. Execution log is generated
        │
        ▼
11. Log is sent through email
        │
        ▼
12. Process repeats after configured interval
```

---

# Repository

GitHub:

https://github.com/bemo-codes/DuplicateFileRemoval

---

# Release

Current stable version:

**v1.0.0**

The `v1.0.0` release represents the first stable version of the project.

---

# License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

# Author

**bemo-codes**

GitHub:

https://github.com/bemo-codes