import os, hashlib, re
from dotenv import load_dotenv
load_dotenv()
VULNSCANNERS_WEBHOOK = os.environ.get('VULNSCANNERS')
REPORTS_DIR= '../reports/'


def get_hash(file_name):
    md5_hash = hashlib.md5()
    a_file = open(file_name, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return(digest)


def ls(folder):
    files = [os.path.join(root, filename)
          for root, dirnames, filenames in os.walk(folder)
          for filename in filenames if filename.endswith('.txt')]
    return files

def reported_vulns():
    with open('reported.txt','r') as f:
        output = f.read()
    output = output.split('\n')
    return [line.strip(' ') for line in output]
    
def read_file_content(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def get_what_is_between(full_string, start, end):
    result = re.search(start+'(.*)'+end, full_string)
    return result.group(1)

def create_exploit_db_report(file_name):
    powerup_file = str(read_file_content(file_name))
    template_file = str(read_file_content('template.txt'))
    service_name = get_what_is_between(powerup_file, "AbuseFunction : Write-ServiceBinary -ServiceName '", "' -Path <HijackPath>")
    template_file = template_file.replace('SERVCIE_NAME_HEHE',service_name)
    bin_name = get_what_is_between(powerup_file, "Path          : ", "\n")
    template_file = template_file.replace('BIN_IS_HERE',bin_name)
    #main_string = get_what_is_between(powerup_file, "ServiceName   :", "HijackPath")
    #template_file = template_file.replace('POWERUPHERE',main_string)

    #template_file = template_file.replace('FILE_NAME_IS_HERE','')

    return(template_file)

def put_in_file(file_name, s):
    text_file = open(file_name, "w")
    n = text_file.write(s)
    text_file.close()

def get_file_name(file_name):
    file_name = file_name.split('/')[-1]
    return file_name

def main():
    reported = reported_vulns()
    files = ls(REPORTS_DIR)
    for file in files:
        hashString = get_hash(file)
        if hashString != "4c490f62f515840ac9d854cedef2cf17":
            if "showalltcplisteningports" not in file:
                if file not in reported:
                    # Notify
                    print("Reported!!")
                    os.system("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"MPS found a vuln using Miner!  "+ str(file) +" \"}' "+str(VULNSCANNERS_WEBHOOK))
                    os.system('echo "'+str(file)+'" >> reported.txt')
                    try:
                        contents = create_exploit_db_report('checks-test.txt')
                        r_file_name = get_file_name(file_name)
                        put_in_file(r_file_name+'-checks-test.txt',contents)
                    except:
                        print("Error 52")
            if "showalltcplisteningports" in file:
                pass

        print("Nothing to report")      

main()