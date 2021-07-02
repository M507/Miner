#!/bin/bash
cd /home/rdpss/

function kill_remmina(){
    #lsfor pid in $(pgrep remmina); do kill $pid; done
    killall remmina
}

function run_remmina(){
    /usr/bin/remmina -c windows.remmina &
}

function main(){

    results=$(curl -s <THE_IP_OF_MPS.domain.com>/START_RDP_SESSION.env)

    if [ $results -eq 0 ]
    then
        echo "Killing rdp .. "
        kill_remmina
        # pgrep remmina
        # if [ $? -eq 0 ]
        # then
        #     echo "Its not running so run it"
        #     kill_remmina
        # fi
    fi

    if [ $results -eq 1 ]
        then
            pgrep remmina
            if [ $? -eq 1 ]
            then
                echo "Killing any old rdp .. "
                kill_remmina
                echo "It's not running so run it"
                run_remmina
            fi
    fi

}

while true; do 
	main
    sleep 2
done
