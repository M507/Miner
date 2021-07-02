import socket, subprocess, sys, psutil, time, os

HOST = 'NO_USED_ANYMORE'
PORT = 7777

mainPS = None

def check_if_mstsc_is_running(): 
    if ("remmina" in (p.name() for p in psutil.process_iter())):
        return True
    return False

def kill_mstsc():
    for p in psutil.process_iter():
        if p.name() == "remmina":
            # try:
            #     mainPS.kill()
            # except:
            #     pass
            # try:
            #     p.kill()
            # except:
            #     pass
            try:
                os.system('python3 k.py')
            except:
                pass
            # time.sleep(2)
            # try:
            #     kill_it()
            # except:
            #     pass

def kill_it():
    # This is risky AF
    # kill -HUP $(ps -A -ostat,ppid | grep -e '[zZ]'| awk '{ print $2 }')
    command = "kill -HUP $(ps -A -ostat,ppid | grep -e '[zZ]'| awk '{ print $2 }')"
    subprocess.Popen(command.split(' '))


def start_rdp():
    pid=os.fork()
    if pid==0: # new process
        os.system("remmina -c /home/rdpss/windows.remmina")
        exit(1)
    # command = "nohup remmina -c /home/rdpss/windows.remmina"
    # subprocess.Popen(command.split(' '), 
    #             stdout=sys.stdout)
    # mainPS = P
    
    
def logic():
    s = socket.socket()
    s.connect((HOST,PORT))
    #s.sendall(data_to_send)
    data = s.recv(1)
    data = data.decode()
    print(data)
    if data == "1":
        if check_if_mstsc_is_running():
            pass
        else:
            print("Starting RDP .. ")
            start_rdp()
    else:
        if check_if_mstsc_is_running():
            print("Killing RDP .. ")
            kill_mstsc() 
    s.close()

def main():
    try:
        kill_mstsc()
        while True:
            print("Executing logic .. ")
            logic()
            print("Waiting 10 seconds .. ")
            time.sleep(10)
    except Exception as e:
        print("Error 1 " + str(e))
        time.sleep(120)
        main()

if __name__ == "__main__":
    pass
    main()
    

