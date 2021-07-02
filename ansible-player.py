import os, subprocess, time, re

def main():
    dropbox = "dropbox"
    list_of_file_to_be_copied = files_ready_to_be_copied(dropbox)
    print(list_of_file_to_be_copied)
    copy_files_to_queue(list_of_file_to_be_copied)


if __name__ == '__main__':
    pass
    #test('dropbox')
    main()
