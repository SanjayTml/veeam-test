import os
import sys
import filecmp
import shutil
import logging
import argparse
from pytimedinput import timedKey

# Global Variables
files_copied = []
files_deleted = []
folders_copied = []
folders_deleted = []
files_modified = []
errors = []

# main sync function
def folder_sync(src, dst):
    # Compare the contents of the source and destination folder
    comparison = filecmp.dircmp(src, dst)

    # Copy files from source to destination that don't exist in destination
    for file in comparison.left_only:
        src_file = os.path.join(src, file)
        dst_file = os.path.join(dst, file)
        log_event("info",f"Copying \'{src_file}\' to destination folder")
        if os.path.isfile(src_file):
            try:
                shutil.copy2(src_file, dst_file)
                files_copied.append(src_file)
                log_event("info","Copying success")
            except PermissionError:
                errors.append(PermissionError)
                log_event("error",f"Permission denied for \'{src_file}\'")
        else:
            try:
                shutil.copytree(src_file, dst_file)
                folders_copied.append(src_file)
                log_event("info","Copying success")
            except PermissionError:
                errors.append(PermissionError)
                log_event("error",f"Permission denied for \'{src_file}\'")

    # Remove files from destination that don't exist in source
    for file in comparison.right_only:
        dst_file = os.path.join(dst, file)
        log_event("info",f"Deleting \'{dst_file}\' from destination folder")
        if os.path.isfile(src_file):
            try: 
                os.remove(dst_file)
                files_deleted.append(dst_file)
                log_event("info","Deletion success")
            except PermissionError:
                errors.append(PermissionError)
                log_event("error",f"Permission denied for \'{dst_file}\'")
        else:
            try:
                shutil.rmtree(dst_file)
                folders_deleted.append(dst_file)
                log_event("info","Deletion success")
            except PermissionError:
                errors.append(PermissionError)
                log_event("error",f"Permission denied for \'{dst_file}\'")

    # Sync the same files with different data in source and destination folder
    for file in comparison.diff_files:
        src_file = os.path.join(src, file)
        dst_file = os.path.join(dst, file)
        # Check if the files are different
        if not filecmp.cmp(src_file, dst_file, shallow=False):
            shutil.copy2(src_file, dst_file)
            files_modified.append(dst_file)
            log_event("info",f"Synced \'{src_file}\' to \'{dst_file}\'")
        else:
            log_event("info",f"File \'{src_file}\' and \'{dst_file}\' are same")

    # Compare the subdirectories in source and destination folder
    for subdir in comparison.common_dirs:
        src_subdir = os.path.join(src, subdir)
        dst_subdir = os.path.join(dst, subdir)
        folder_sync(src_subdir, dst_subdir)


# calls sync function periodically
def sync_in_interval(src, dst, interval):
    log_event("info","Sync starts..")
    while True:
        folder_sync(src, dst)
        log_event("info",f"Copied {len(files_copied)} files, deleted {len(files_deleted)} files, modified {len(files_modified)} files.")
        log_event("info",f"Copied {len(folders_copied)} folders, deleted {len(folders_deleted)} folders.")
        log_event("info",f"Total errors: {len(errors)}")
        log_event("info","Sync complete!")
        print(f"Next sync in {interval} seconds")
        ask_for_quit(interval)
        

# asks user to quit the sync program with timeout
def ask_for_quit(interval):
    userText, timedOut = timedKey("(Press q to exit or c to continue)", timeout=interval,allowCharacters="qc")
    if(timedOut):
        log_event("info", "Sync starts..")
    else:
        if(userText == "q"):
            print("Quiting Program..")
            sys.exit(0)

# logs the message and prints it in console
def log_event(level, message):
    # Log the message
    if level == 'debug':
        logging.debug(f'{message}')
    elif level == 'info':
        logging.info(f'{message}')
    elif level == 'warning':
        logging.warning(f'{message}')
    elif level == 'error':
        logging.error(f'{message}')
    elif level == 'critical':
        logging.critical(f'{message}')
    # print it in the console
    print(f"{message}")

if __name__ == '__main__':
    # Get source and destination folder from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="path to the source folder")
    parser.add_argument("dst", help="path to the replica folder")
    parser.add_argument("-i", "--interval", help="time interval in seconds between each sync", type=int, default=60)
    parser.add_argument("-l", "--logfile", help="path to the log file", default='sync.log')
    args = parser.parse_args()
    logging.basicConfig(filename=args.logfile, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    print(f"Logging to the file {args.logfile} with sync interval of {args.interval} seconds")
    # Call the function to synchronize periodically in intervals
    sync_in_interval(args.src, args.dst, args.interval)
