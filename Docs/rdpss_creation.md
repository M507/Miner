## Ubuntu 20

### Execute this also in the Windows system so it remambers the password and does't ask for it everytime.
```sh
cmdkey /generic:THE_IP_OF_WINDOWS /user:"Administrator" /pass:"password123"
```
### Then start the service
start-service run_miner_rdp_checker

