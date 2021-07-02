import os, subprocess, time, re


def execute_cmd(command):
    out = subprocess.Popen(command.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    return stdout.decode()


def execute_cmd_return_lines_in_a_list_and_delete_the_first_3_lines(command):
    """
    For (ls -la) commands only
    :param command:
    :return:
    """
    out = subprocess.Popen(command.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    output_lines =  stdout.decode().split('\n')
    return [re.sub(' +', ' ', line.replace('\n', '').replace('\r', '')) for line in output_lines if len(line) > 0][3:]

def execute_cmd_return_lines_in_a_list(command):
    """
    For the rest of commands
    :param command:
    :return:
    """
    out = subprocess.Popen(command.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    output_lines = stdout.decode().split('\n')
    return [re.sub(' +', ' ', line.replace('\n', '').replace('\r', '')) for line in output_lines if len(line) > 0]


def get_file_hash(dropbox_dir, filename):
    """
    Get md5hash of a file.

    :param dropbox_dir:
    :param filename:
    :return:
    """
    command = "md5sum "+ dropbox_dir + '/' + get_filename(filename)
    # Get the first line
    line = execute_cmd_return_lines_in_a_list(command)[0]
    # Get the first chunk
    return line.split(' ')[0]


def get_filename(line):
    """
    Get file name from ls -la
    :param line:
    :return:
    """
    return line.replace('\n','').replace('\r','').strip(' ').split(' ')[-1]


def files_ready_to_be_copied(dropbox_dir):
    """
    Get a list of filenames that are ready to be copied + are not currently downloading
    :param dropbox_dir:
    :return:
    """
    list_of_file_with_sizes = []
    list_of_file_to_be_copied = []
    output_lines = execute_cmd_return_lines_in_a_list_and_delete_the_first_3_lines("ls -lah " + dropbox_dir+'/')

    for line in output_lines:
        hash = str(get_file_hash(dropbox_dir, line))
        tmp_filename_1 = get_filename(line)
        pair = [tmp_filename_1, hash]
        list_of_file_with_sizes.append(pair)

    print("Waiting to compare")
    # This is a check in case I am uploading files, so it doesn't copy files that I am currently uploading.
    time.sleep(20)
    output_lines = execute_cmd_return_lines_in_a_list_and_delete_the_first_3_lines("ls -lah " + dropbox_dir + '/')
    for line in output_lines:
        hash = str(get_file_hash(dropbox_dir, line))
        tmp_filename_1 = get_filename(line)
        for pair in list_of_file_with_sizes:
            tmp_filename_2 = pair[0]
            tmp_hash = pair[1]
            if tmp_filename_1 == tmp_filename_2:
                if hash == tmp_hash:
                    list_of_file_to_be_copied.append('dropbox/' + tmp_filename_1)

    return (list_of_file_to_be_copied)

def get_last_used_number():
    """
    Get the last number used in queue dir.
    :return:
    """
    try:
        output_lines = execute_cmd_return_lines_in_a_list_and_delete_the_first_3_lines("ls -lah queue/")
        largest = 0
        for file in output_lines:
            tmp_filename_1 = get_filename(file)
            number = int(tmp_filename_1.split('_')[2])
            if number > largest:
                largest = number
        return largest
    except:
        print("Error 251")
        return None


def copy_files_to_queue(list_of_file_to_be_copied):
    """
    Copy files to queue with uniq names
    :param list_of_file_to_be_copied:
    :return:
    """
    # Get the last file
    try:
        number = int(get_last_used_number())
        for file in list_of_file_to_be_copied:
            # Increase it by one
            number += 1
            only_the_file_name = file.split('/')[-1]
            command = 'mv '+ file +' queue/m_install_' + str(number) + '_'+ only_the_file_name
            output_lines = execute_cmd_return_lines_in_a_list(command)
    except:
        print("Error 251")
        return None

def test(dropbox):
    pass
    get_file_hash('dropbox','a.txt')

def rename_all_files(path):
    filenames = os.listdir(path)
    for filename in filenames:
        os.rename(os.path.join(path, filename), os.path.join(path, filename.replace(' ', '-')))

def main():
    dropbox = "dropbox"
    print("Renaming files")
    rename_all_files(dropbox)
    list_of_file_to_be_copied = files_ready_to_be_copied(dropbox)
    print("Listing all files")
    print(list_of_file_to_be_copied)
    print("Copying files")
    copy_files_to_queue(list_of_file_to_be_copied)


if __name__ == '__main__':
    pass
    #test('dropbox')
    main()