import sys
import re
import os
import schedule
import time
import hashlib
import smtplib
from datetime import datetime

from email.message import EmailMessage

def CalculateCheckSum(FileName):

    if not os.path.exists(FileName):
        raise FileNotFoundError(f"File does not exist: {FileName}")

    if not os.path.isfile(FileName):
        raise ValueError(f"Path is not a regular file: {FileName}")

    if not os.access(FileName, os.R_OK):
        raise PermissionError(f"File is not readable: {FileName}")    
    try:
        fobj = open(FileName, "rb")
        hobj = hashlib.md5()

        Buffer = fobj.read(1024)

        while len(Buffer)>0:
            hobj.update(Buffer)
            Buffer = fobj.read(1024)

        fobj.close()
        return hobj.hexdigest()
    except OSError as e:
        print("Directory doesn't exist.")
        return

def FindDuplicate(Directory):
    
    if not os.path.exists(Directory):
        print("Directory does not exist.")
        return 

    if not os.path.isdir(Directory):
        print("The supplied path is not a directory.")
        return 

    if not os.access(Directory, os.R_OK | os.X_OK):
        print("Application does not have permission to access the directory.")
        return

    Duplicate = {}
    
    for FolderName, SubFolder, FileName in os.walk(Directory):
        for fname in FileName:
            fname = os.path.join(FolderName, fname)

            if not os.path.exists(fname):
                continue

            if not os.path.isfile(fname):
                continue

            if not os.access(fname, os.R_OK):
                print(f"File is not readable: {fname}")
                continue
            try:
                CheckSum = CalculateCheckSum(fname)

                if CheckSum in Duplicate:
                    Duplicate[CheckSum].append(fname)
                else:
                    Duplicate[CheckSum] = [fname]
            except(PermissionError,OSError,ValueError) as e:
                print(f"Unable to process file {fname} \n Reason: {e}")

    return Duplicate

def DeleteDuplicate(DirectoryName):
    border = "-"*50
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M:%S.%f %p")

    LogfileName = f"LogFile{timestamp}.log"
    LogfileName = LogfileName.replace(" ","_")
    LogfileName = LogfileName.replace(":","_")

    fobj = open(LogfileName, "w")

    fobj.write(border + "\n")
    fobj.write(" Automation Script \n")
    fobj.write(border + "\n")
    
    fobj.write("Files inside the directory are: \n\n")
    fobj.write(border + "\n")

    MyDict = FindDuplicate(DirectoryName)
    print(MyDict)

    TotalFiles = 0
    for key in MyDict:
        for value in MyDict[key]:
            TotalFiles += 1

    Result = list(filter(lambda x: len(x)>1, MyDict.values()))

    count = 0
    TotalDeleted = 0
    duplicate = 0
    
    for value in Result:
        for subvalue in value:
            count += 1
            if count>1:
                duplicate +=1
                CheckSum = CalculateCheckSum(subvalue)
                fobj.write(f"Deleted duplicate file: {subvalue} \n")
                fobj.write(f"Checksum is: {CheckSum}\n")

                if not os.path.exists(subvalue):
                    fobj.write(f"{subvalue} no longer exists.\n\n")
                    continue  

                if not os.path.isfile(subvalue):
                    fobj.write(f"{subvalue} is not a regular file.\n\n")
                    continue

                if not os.access(subvalue, os.W_OK):
                    fobj.write(f"{subvalue} cannot be deleted because permission is denied.\n\n")
                
                try:
                    os.remove(subvalue)
                    TotalDeleted += 1
                    fobj.write(f"{subvalue} deleted successfully. \n\n")
                except Exception as e:
                    fobj.write(f"Error while deleting the file: {e} \n\n")
        count = 0

    timestamp1 = datetime.now().strftime("%d %b %Y, %I:%M:%S.%f %p")

    fobj.write(border + '\n')
    fobj.write(f"Starting time of the directory scanning: {timestamp}\n")
    fobj.write(f"Completion time of directory scanning: {timestamp1}\n")
    fobj.write(f"Directory scanned: {DirectoryName}\n")
    fobj.write(f"Total Files scanned: {TotalFiles}\n")
    fobj.write(f"Duplicate files found: {duplicate}\n")
    fobj.write(f"Deleted duplicate files: {TotalDeleted}\n")
    fobj.close()

    return timestamp, timestamp1, DirectoryName, TotalFiles, duplicate, TotalDeleted, LogfileName

def ValidateEmail(ReceiverEmail):

    if ReceiverEmail == "":
        print("Email address is required.")
        return False

    # Basic email format validation
    EmailPattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(EmailPattern, ReceiverEmail): 

        print("Invalid email address format.")
        return False

    return True

def SendEmail(ReceiverEmail, timestamp, timestamp1, DirectoryName,
              TotalFiles, duplicate, TotalDeleted, LogfileName):

    SenderEmail = os.environ.get("GMAIL_USER")
    SenderPassword = os.environ.get("GMAIL_APP_PASSWORD")

    if not ValidateEmail(ReceiverEmail):
        return

    if not SenderEmail:
        print("GMAIL_USER environment variable is not set.")
        return

    if not SenderPassword:
        print("GMAIL_APP_PASSWORD environment variable is not set.")
        return

    msg = EmailMessage()

    msg["From"] = SenderEmail
    msg["To"] = ReceiverEmail
    msg["Subject"] = "Duplicate file Removal Report"

    Body = f'''
The duplicate-file removal operation has been completed successfully.

Operation Statistics:

Starting time of scanning: {timestamp}
Completion time of scanning: {timestamp1}
Directory scanned: {DirectoryName}
Total number of files scanned: {TotalFiles}
Total number of duplicate files found: {duplicate}
Total number of duplicate files deleted: {TotalDeleted}

Please find the detailed log file attached to this email.

Regards,
Automation System
'''
    msg.set_content(Body)

    if not os.path.exists(LogfileName):
        print("Log file does not exist. Email cannot be sent.")
        return
    try:
        fobj = open(LogfileName, "rb")
        FileData = fobj.read()
    
        msg.add_attachment(
            FileData,
            maintype='text',
            subtype='plain',
            filename=LogfileName
        )
    except PermissionError:
        print("Permission denied while reading log file.")
        return

    except OSError as e:
        print(f"Unable to read log file: {e}")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(
                SenderEmail,
                SenderPassword
            )
            smtp.send_message(msg)
        print("Email sent successfully.")

    except smtplib.SMTPAuthenticationError:
        print("Email authentication failed. \n Check your Gmail address and App Password.")
            
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred while sending email: {e}")
          
    except OSError as e:
        print(f"Network error while sending email: {e}")
        
def PerformOperation(DirectoryName, ReceiverEmail):

    timestamp, timestamp1, DirectoryName, TotalFiles, duplicate, TotalDeleted, LogfileName = DeleteDuplicate(DirectoryName)

    SendEmail(
        ReceiverEmail,
        timestamp,
        timestamp1,
        DirectoryName,
        TotalFiles,
        duplicate,
        TotalDeleted,
        LogfileName
    )

def ValidateDirectory(DirectoryName):

    if DirectoryName == "":
        print("Directory path is required.")
        return False

    if not os.path.isabs(DirectoryName):
        print("Directory path must be an absolute path.")
        return False

    if not os.path.exists(DirectoryName):
        print("Directory does not exist.")
        return False

    if not os.path.isdir(DirectoryName):
        print("The supplied path is not a directory.")
        return False

    if not os.access(DirectoryName, os.R_OK | os.X_OK):

        print("Application does not have permission to access the directory.")
        return False
    return True


def ValidateInterval(IntervalValue):

    # Check whether interval is provided
    if IntervalValue == "":
        print("Time interval is required.")
        return None
    try:
        Interval = float(IntervalValue)

    except ValueError:
        print("Time interval should contain only a valid numeric value. ")
        return None

    # Interval must be greater than zero
    if Interval <= 0:
        print("Time interval should be greater than zero.")
        return None
    return Interval

def DisplayHelp():

    print("""
Duplicate File Removal Automation

This script:
1. Scans a directory.
2. Identifies duplicate files using MD5 checksums.
3. Deletes duplicate files.
4. Creates a log file.
5. Sends the log file through email.

Usage:

python duplicate_file_remover.py <DirectoryPath> <IntervalInMinutes> <ReceiverEmail>
Enter <DirectoryPath> as a string i.e. in double/single quotes.

Options:

-h
--help

Display help information.

-u
--usage

Display usage information.
""")

def main():
    border = "-"*50
    print(border)
    print("Automation Script")
    print(border)

    if len(sys.argv) == 1:
        print("Invalid number of arguments.")
        print("Please use '-h' or '-u' for more information.")
        return

    if len(sys.argv) == 2:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h" :
            DisplayHelp()
            return
            
        elif sys.argv[1] == "--usage" or sys.argv[1] == "-u":
            print('''
    Usage: \n
    python Assignment33.py <DirectoryPath> <IntervalInMinutes> <RecieverEmail> ''')

    if len(sys.argv) != 4:
        print("Invalid number of arguments.")
        print("Please use '-h' or '-u for more information.")
        return  

    DirectoryName = sys.argv[1]
    IntervalValue = sys.argv[2]
    ReceiverEmail = sys.argv[3]

    if not ValidateDirectory(DirectoryName):
        return

    Interval = ValidateInterval(IntervalValue)
    if Interval is None:
        return 

    if not ValidateEmail(ReceiverEmail):
        return

    print("Directory validation successful.")
    print("Time interval validation successful.")
    print("Email validation successful.")

    print(f"Duplicate file removal operation scheduled every {Interval} minute(s).")

    schedule.every(Interval).minutes.do(
        PerformOperation,
        DirectoryName,
        ReceiverEmail
    )
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
