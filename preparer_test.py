import os
from os import listdir
from os.path import isfile, join


def get_list_of_queue_files(queue):
    files = [queue+ '/' +f for f in listdir(queue) if isfile(join(queue, f))]
    files = [ file for file in files if "m_install_" in file ]
    return files


def check_if_tested_before_file(full_file_name, file_name):
    completed_files = get_list_of_queue_files("completed")
    for current_file_name in completed_files:
        current_file_name = get_just_the_file_name(current_file_name)
        if s_compare(current_file_name,file_name):
            return True
    return False

def get_only_program_name(file_name):
    #file_name = ''.join([i for i in file_name if not i.isdigit()])
    file_name = file_name.split('/')[-1]
    file_name = file_name.replace('m_install_','')
    toberemoved = file_name.split('_')[0]
    file_name = file_name.replace(toberemoved,'')[1:]
    return file_name


def get_list_of_file_names(files):
    new_list_of_files = []
    for file in files:
        try:
            new_list_of_files.append(get_only_program_name(file)+'\n')
        except:
            pass
    return new_list_of_files


# files = get_list_of_queue_files("completed")

# new_list_of_files = get_list_of_file_names(files)

# f = open("completed.txt", "a")
# f.writelines(new_list_of_files)
# f.close()



def set_completed_file(full_file_name, file_name):
    command = 'mv '+ full_file_name +' /tmp/'+ file_name
    file_name = get_only_program_name(file_name)
    print(command)
    if Run:
        os.system(command)
    command = 'echo "' + file_name + '" >> completed/completed.txt'
    print(command)
    if Run:
        os.system(command)


def read_all_lines(file_name):
    with open(file_name,'r') as f:
        output = f.read()
    return output.split('\n')


def check_if_tested_before(file_name):
    files = read_all_lines('completed/completed.txt')
    return file_name in files


append_to_file('completed/completed.txt','line')
