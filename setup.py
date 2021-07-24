import os



def mkdir_list(dirs):
    for d in dirs:
        os.system('mkdir '+d)


def main():
    dirs = ['reports', 'queue','logs','dropbox','completed']
    mkdir_list(dirs)



main()
