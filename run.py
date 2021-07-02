import os
from os import listdir
from os.path import isfile, join

Run = 1

def get_list_of_queue_files(queue):
    files = [queue+ '/' +f for f in listdir(queue) if isfile(join(queue, f))]
    files = [ file for file in files if "m_install_" in file ]
    return files


def get_list_of_queue_files_no_full_path(queue):
    files = [ f for f in listdir(queue) if isfile(join(queue, f))]
    files = [ file for file in files if "m_install_" in file ]
    return files


def get_priority_number(file_name):
    priority_number = file_name.split('_')[2]
    return priority_number


def get_first_in_queue(queue):
    files = get_list_of_queue_files(queue)
    the_first = None
    for file in files:
        priority_number = int(get_priority_number(file))
        if the_first is None:
            the_first = priority_number
            continue
        if priority_number < the_first:
            the_first = priority_number
    
    if the_first != None:
        return get_file_by_priority_number(queue, the_first)
    return None


def get_file_by_priority_number(queue, priority_number):
    files = get_list_of_queue_files(queue)
    for file_name in files:
        current_priority_number = int(get_priority_number(file_name))
        if current_priority_number == priority_number:
            return file_name
    return None


def get_just_the_file_name(file_name):
    return file_name.split('/')[1]


def get_rid_of_prefix(file_name):
    return file_name.replace('m_install_','')[2:]


def check(target):
    data = [(int(p), c) for p, c in [x.rstrip('\n').split(' ', 1) for x in os.popen('ps h -eo pid:1,command')]]
    # Check if it's already running
    counter = 0
    for e in data:
        if target in e[1]:
            counter += 1
            print(e)
        
    if counter >= 4:
        print(counter)
        print("Leaving")
        exit(1)


def s_compare(current_file_name,file_name):
    current_file_name = ''.join([i for i in current_file_name if not i.isdigit()])
    file_name = ''.join([i for i in file_name if not i.isdigit()])
    current_file_name = current_file_name.replace('m_install__','')
    file_name = file_name.replace('m_install__','')
    return current_file_name == file_name


def read_all_lines(file_name):
    with open(file_name,'r') as f:
        output = f.read()
    return output.split('\n')


def check_if_tested_before(file_name):
    file_name = get_only_program_name(file_name)
    files = read_all_lines('completed/completed.txt')
    return file_name in files


def get_only_program_name(file_name):
    file_name = file_name.split('/')[-1]
    file_name = file_name.replace('m_install_','')
    toberemoved = file_name.split('_')[0]
    file_name = file_name.replace(toberemoved,'')[1:]
    return file_name


def append_to_file(file_name,line):
    file1 = open(file_name, "a")
    file1.write(line+"\n") 
    file1.close() 


def set_completed_file(full_file_name, file_name):
    if Run:
        src= './'+full_file_name
        dest = '/tmp/'+ file_name
        command = "mv "+src+' '+dest
        os.system(command)
    file_name = get_only_program_name(file_name)
    append_to_file('completed/completed.txt',file_name)


def run(file_name, modules):
    
    for module in modules:
        command = 'ansible-playbook site.yml -i inventory.ini --extra-vars "file_name=' + file_name + ' run_version=' + module +'"'
        print(command)
        if Run:
            pass
            os.system(command)


def main():
    # static values that shouldn't be changed
    dropbox = "dropbox"
    queue = "queue"
    ddone_folder = "completed"

    # These are the Python scripts that will run to install the exe file.
    modules = ["main","main_keys"]

    full_file_name = get_first_in_queue(queue)
    if full_file_name != None:
        file_name = get_just_the_file_name(full_file_name)
        if file_name != None:            
            print("Checking if this file has been tested before...")
            # Check if this file has been tested before.
            if check_if_tested_before(file_name):
                print("Yes it has been tested!")
                try:
                    set_completed_file(full_file_name, file_name)
                except Exception as ex:
                    print(ex)
                    print("Error 37")
            # If it's new... work your ass off
            else:
                try:
                    print("Running")
                    run(file_name, modules)
                except Exception as ex:
                    print(ex)
                    print("Error 42")
                try:
                    print(file_name)
                    set_completed_file(full_file_name, file_name)
                except Exception as ex:
                    print(ex)
                    print("Error 72")
    else:
        print("No work to do.")
        exit(1)    


if __name__ == '__main__':
    pass
    target = "ansible-playbook"
    check(target)
    try:
        while True:
            main()
    except Exception as ex:
        print(ex)
        print("Exited with error 0")
        exit(0)