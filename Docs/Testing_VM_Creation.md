### Create a new user without any admin privs.
```powershell
net user lowprivuser /add
net user lowprivuser Password-123*
net user Administrator "password123"
net user Administrator /active
net localgroup "Remote Management Users" /add lowprivuser
```

### Enable running scripts
```powershell
Set-ExecutionPolicy unrestricted
```

### Enable winrm
```powershell

winrm quickconfig
$RemoteHostName = $ENV:ComputerName
$ComputerName = $ENV:ComputerName
 
Write-Host "Setup WinRM for $RemoteHostName"

$Cert = New-SelfSignedCertificate -DnsName $RemoteHostName, $ComputerName `
    -CertStoreLocation "cert:\LocalMachine\My" 

$Cert | Out-String

$Thumbprint = $Cert.Thumbprint

Write-Host "Enable HTTPS in WinRM"
$WinRmHttps = "@{Hostname=`"$RemoteHostName`"; CertificateThumbprint=`"$Thumbprint`"}"
winrm create winrm/config/Listener?Address=*+Transport=HTTPS $WinRmHttps

Write-Host "Set Basic Auth in WinRM"
$WinRmBasic = "@{Basic=`"true`"}"
winrm set winrm/config/service/Auth $WinRmBasic


Write-Host "Open Firewall Port"
netsh advfirewall firewall add rule name="Windows Remote Management (HTTPS-In)" dir=in action=allow protocol=TCP localport=$WinRmPort


winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/client/auth '@{Basic="true"}'


winrm enumerate winrm/config/listener
```

### Turn off the UAC
```powershell

reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
shutdown /r /t 0
```


#### Install NSSM using choco - Google it


Now to run the script we only need to execute this command:
```powershell
Start-Service startpowerup0
```

### Install psexec
Download https://docs.microsoft.com/en-us/sysinternals/downloads/psexec
Copy PsExec.exe to system32

