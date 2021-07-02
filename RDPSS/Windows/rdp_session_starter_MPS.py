#p23_server.py
import socket, time

HOST = 'NO_USED_ANYMORE'
PORT = 7777

def get_START_RDP_SESSION():
    with open('/var/www/html/START_RDP_SESSION.env','r') as f:
        output = f.read()
        output = output.strip(' ').replace('\n','').replace('\r','')
    return output


def logic():
    print("Starting the server")
    server = socket.socket()
    server.bind((HOST,PORT))
    server.listen(0)
    print("Waiting .. ")
    (client,addr) = server.accept()
    print("Accepted")
    try:
        print("Checking .. ")
        data = str(get_START_RDP_SESSION())
        print("Sending .. "+str(data))
        client.send(data)
    except:
        pass
        print("Error")
    # Wait a second better than waiting for "time-wait" at 7777
    time.sleep(1)
    server.close()

def main():
    try:
        while True:
            logic()
            time.sleep(8)
    except:
        pass
        print("ERRER!!!!!!")
        print("Wait for 120 seconds and restart..")
        time.sleep(120)
        main()


if __name__ == "__main__":
    pass
    main()