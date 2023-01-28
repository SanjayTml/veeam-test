# veeam-test (Folder Synchronization)
This program is designed to synchronize the contents of a source folder with a destination folder. The program compares the contents of the two folders and copies new or modified files from the source folder to the destination folder, and deletes files from the destination folder that do not exist in the source folder. It also recursively compares and synchronizes subdirectories within the source and destination folders.

### Features
- Compares the contents of a source folder with a destination folder
- Copies new or modified files from the source folder to the destination folder
- Deletes files from the destination folder that do not exist in the source folder
- Recursively compares and synchronizes subdirectories within the source and destination folders
- Logs events and errors during the synchronization process
- Asks the user to quit the program with a timeout feature

### Required Libraries
- os
- sys
- filecmp
- shutil
- logging
- argparse
- pytimedinput

### Usage
The program can be executed by running the command below:
``` 
python sync.py -src <source_folder> -dst <destination_folder> -i <interval> -l <log_file>
```

src : Path to the source folder
dst : Path to the destination folder
i : Interval in seconds at which the synchronization process should be run
l : Path to the log file

### Logging
The program logs all events and errors during the synchronization process. The log files are stored in the same directory as the program and are named as sync_log.log.

### Exiting the program
The program periodically asks the user to quit the program with a timeout feature. If the user enters 'q' the program exits otherwise it continues to run the sync process.