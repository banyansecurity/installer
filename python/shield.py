""" Banyan Shield """

import os
import json
import re
import sys
from time import strftime, localtime, time

from common import SLEEP, get_machine_details, successful_install, is_file_empty, run_cmd, parse_argv
from common import install_docker
from config import SHIELD



def install_shield(machine_details):

    shield_version = machine_details["shield"]
    shield_org_id = machine_details["shield_orgid"]
    shield_name = machine_details["shield_name"]      

    download_url = "https://www.banyanops.com/netting/" 
    if "-rc" in shield_version:
        download_url = "https://www-stage.bnntest.com/netting/"

    os.system("echo '==> Starting Shield installation, version: %s from: %s'" % (shield_version, download_url))

    # Install Docker first
    install_docker()

    # Now install Shield
    os.system("wget " + download_url + "deploy-shield-ca-" + shield_version + ".tar.gz")
    os.system(SLEEP)
    os.system("tar zxvf deploy-shield-ca-" + shield_version + ".tar.gz")
    os.system(SLEEP)

    # descend into the shield dir
    cwd = os.getcwd()
    deploy_dir = cwd + "/deploy-shield-ca/"
    os.chdir(deploy_dir)

    with open('start-shield-ca.sh', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if re.search(r'CM=', line):
                line = line.replace('<cm type>', 'none')
            elif re.search(r'GROUPTYPE=', line):
                line = line.replace('<type of deployment>', 'test')
            elif re.search(r'ORG_ID=', line):
                line = line.replace('<organization id>', shield_org_id)
            elif re.search(r'CNAME=', line):
                line = line.replace('<cluster name>', shield_name)
            elif re.search(r'TLSNOVERIFY=', line):
                line = line.replace('<true/false>', 'true')

            f.write(line)

    # always stop and delete the existing token
    os.system('./stop-shield-ca.sh')
    os.system('sudo rm /home/vagrant/.banyan/shield/*')
    # then start
    os.system('./start-shield-ca.sh true')
    os.chdir(cwd)

    shield_data = {
        "ORG_ID": shield_org_id,
        "Shield_Address": SHIELD,
        "Shield_Version": shield_version,
        "Timestamp": strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    }
    successful_install("shield_params.json", shield_data)
    return True


def check_shield_installed(machine_details):
    shield_match = False
    req_shield_version = machine_details.get("shield", False)
    
    shield_file_exists = os.path.isfile("shield_params.json")
    if shield_file_exists:
        with open("shield_params.json") as data_file:
            cur_shield_data = json.load(data_file)

        cur_shield_version = cur_shield_data.get("Shield_Version")
        if req_shield_version == cur_shield_version:
            shield_match = True

    return shield_match


def stop_shield():
    if os.path.isdir("/home/vagrant/deploy-shield-ca"):
        os.chdir("/home/vagrant/deploy-shield-ca/")
        os.system('./stop-shield-ca.sh')
        os.chdir("/home/vagrant")
    return True


def start_shield():
    os.chdir("/home/vagrant/deploy-shield-ca/")
    os.system('./start-shield-ca.sh')
    os.chdir("/home/vagrant")
    return True


def manage(machine_details):
    shield_match = check_shield_installed(machine_details)

    if machine_details.get("shield", False):
        if not shield_match:
            install_shield(machine_details)
            os.system("echo '==> Shield installed'")
        else:
            stop_shield()
            start_shield()
            os.system("echo '==> Shield installed, correct version, restarting'")
    else:
        stop_shield()
        os.system("echo '==> Shield stopped / not installed '")          


def health_check():
    table_data = list()

    # shield    
    runcmd = "bash -c \"sudo docker ps --format '{{.Image}}' | grep shield\""
    shield, status = run_cmd(cmd=runcmd)

    shield_status = "1, Banyan Shield, Not Installed"
    if status == 0:
        shield_status = "0, Banyan Shield %s, %s" % (shield.strip(), "Running")
    else:
        shield_status = "1, Banyan Shield, %s" % "Exited"
    
    table_data.append(shield_status)

    # cfssl
    runcmd = "bash -c \"sudo docker ps --format '{{.Image}}' | grep cfssl\""
    cfssl, status = run_cmd(cmd=runcmd)

    cfssl_status = "1, Banyan Shield-CFSSL, Not Installed"
    if status == 0:
        cfssl_status = "0, Banyan Shield-CFSSL %s, %s" % (cfssl.strip(), "Running")
    else:
        cfssl_status = "1, Banyan Shield-CFSSL, %s" % "Exited"
    
    table_data.append(cfssl_status)

    return "\n".join(table_data)    



if __name__ == "__main__":
    my_ip, health = parse_argv()
    machine_details, machines = get_machine_details(my_ip)    

    if health:
        table_data = list()
        table_data.append(health_check())
        print "\n".join(table_data)

    else:
        manage(machine_details)
