## Install 
```
yum update -y
yum install epel-release -y
yum install httpd git vim tmux python-pip wget -y
pip install ansible
pip install pyvmomi
pip install pywinrm
ansible-galaxy collection install community.vmware
yum groupinstall "Development Tools"
systemctl start httpd
systemctl enable httpd
```


## Firewall
```
firewall-cmd --permanent --zone=public --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="80" accept'
firewall-cmd --reload
```


## This is a must:
```sh
[root@mining-project-storage exe_finder]# ls -la /var/www/html/START_RDP_SESSION.env 
-rw-rw-rw-. 1 root root 2 Nov 29 04:13 /var/www/html/START_RDP_SESSION.env
[root@mining-project-storage exe_finder]# 
```


### Real start just edit your crontab:
### Add these:
```sh
*/5 * * * * cd /opt/Miner;python run.py >> logs/run_general.txt
*/5 * * * * cd /opt/Miner;python preparer.py >> logs/prepare_general.txt
*/5 * * * * cd /opt/Miner/GithubScanner;python3 github-url-grapper.py >> ../logs/github-url-grapper_general.txt
0 * * * * cd /opt/Miner/notifier;python3 notifier.py >> ../logs/notifier_general.txt
```

Or run them manually:

```
# start by downloading files manually, exit when done
cd /opt/Miner/GithubScanner;python3 github-url-grapper.py 
# copy and preparer the downloaded files 
cd /opt/Miner;python preparer.py
# finally, run Miner
cd /opt/Miner;python run.py
```


### Debug:
```sh
ansible-playbook site.yml -i inventory.ini --extra-vars "file_name=test run_version=main"
ansible-playbook site.yml -i inventory.ini --extra-vars "file_name=Vembu_BDR_Backup_Server_Setup_4_2_0_1_U1_GA.exe run_version=main_keys"
```
