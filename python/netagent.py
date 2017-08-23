""" Banyan Netagent """

import os
import json
import re
from time import strftime, localtime, time

from common import SLEEP, get_machine_details, successful_install, is_file_empty, run_cmd, parse_argv
from config import NETAGENT_SERVER_CIDRS, SHIELD



GPG_PASSWORD = "gobany@n"
DISABLE_L7 = "true"


def install_netagent(machine_details):

    netagent_version = "netagent-" + machine_details["netagent"]

    download_url = "https://www.banyanops.com/netting/" 
    if "-rc" in netagent_version:
        download_url = "https://www-stage.bnntest.com/netting/"

    os.system("echo '==> Starting Netagent installation, version: %s from: %s'" % (netagent_version, download_url))

    NETAGENT_INSTALL_COMMANDS = [
        "sudo apt-get update -qq",
        "wget " + download_url + netagent_version + ".tar.gz",
        "sleep 1",
        "tar zxf " + netagent_version + ".tar.gz",
        "sleep 1"
    ]
    
    for index, command in enumerate(NETAGENT_INSTALL_COMMANDS):
        os.system(command)

    # descend into the netagent dir    
    cwd = os.getcwd()
    netagent_dir = cwd + "/"+ netagent_version + "/"
    os.chdir(netagent_dir)
    os.system("cp config-netagent.tpl config-netagent")

    with open('config-netagent', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if re.search(r'shield_addr=', line):
                line = line.replace('127.0.0.1', SHIELD[0])
            elif re.search(r'gpg_password=', line):
                line = line.replace('REPLACE', GPG_PASSWORD)
            elif re.search(r'disable_L7=', line):
                line = line.replace('false', DISABLE_L7)
            f.write(line)
    
    # don't setup here, run in cidr step
    # os.system('./setup-netagent.sh')
    os.chdir(cwd)

    netagent_data = {
        "Netagent_Version": netagent_version,
        "Timestamp": strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    }
    successful_install("netagent_params.json", netagent_data)
    return True


def check_netagent_installed(machine_details):
    netagent_match = False
    req_netagent_version = "netagent-" + str(machine_details.get("netagent", False))

    netagent_file_exists = os.path.isfile("netagent_params.json")
    if netagent_file_exists == True:
        with open("netagent_params.json") as data_file:
            cur_netagent_data = json.load(data_file)

        cur_netagent_version = cur_netagent_data.get("Netagent_Version")
        if req_netagent_version == cur_netagent_version:
            netagent_match = True

    return netagent_match    


def set_netagent_cidrs(machine_details):

    netagent_version = "netagent-" + machine_details["netagent"]
    netagent_role = machine_details.get("netagent_role", "None")

    # descend into the netagent dir    
    cwd = os.getcwd()
    netagent_dir = cwd + "/"+ netagent_version + "/"
    os.chdir(netagent_dir)

    # Netagent on client nodes
    if netagent_role == "client":
        os.system('echo "" > client-cidr.txt')
        for i in range(len(NETAGENT_SERVER_CIDRS)):
            os.system('echo ' + NETAGENT_SERVER_CIDRS[i] + ' >> client-cidr.txt')

    # Netagent on server nodes
    if "server" in netagent_role:
        os.system('echo "" > server-cidr.txt')
        ports = netagent_role.split("-")
        if len(ports) < 2:
            raise ValueError, "Please specify server ports; ex: 'server-1234-9999'"
        for port in ports[1:]:
            os.system('echo ' + machine_details["ip"] + ' --dport ' + port + ' >> server-cidr.txt')
 
    os.system('./setup-netagent.sh')
    os.chdir(cwd)



def start_netagent():
    os.system("sudo initctl start netagent")
    return True


def stop_netagent():
    os.system("sudo initctl stop netagent")
    return True


def manage(machine_details):
    netagent_match = check_netagent_installed(machine_details)

    if machine_details.get("netagent", False):
        if not netagent_match:
            install_netagent(machine_details)
            set_netagent_cidrs(machine_details)
            os.system("echo '==> Netagent installed, CIDRs set'")
        else:
            stop_netagent()
            set_netagent_cidrs(machine_details)
            os.system("echo '==> Netagent already installed, correct version, updating CIDRs and restarting'")
    else:
        stop_netagent()
        os.system("echo '==> Netagent stopped / not installed '")          


def health_check():
    netagent_version_cmd = "sudo /opt/banyan/netagent -v"
    netagent_status_cmd = "sudo initctl status netagent"
    netagent_version, status1 = run_cmd(cmd=netagent_version_cmd, popen=True)
    netagent_status, status2 = run_cmd(cmd=netagent_status_cmd)
    
    health_status = "1, Banyan Netagent, Not Installed"
    if status1 == 0 and status2 == 0:
        procname = netagent_version.split("\n")[0].strip()
        initctl = netagent_status.split("\n")[0].strip()
        if "stop" in netagent_status:
            health_status = "1, %s, %s" % (procname, initctl)
        else:
            health_status = "0, %s, %s" % (procname, initctl)
    else:
        health_status = "1, %s, %s" % (netagent_version.split("\n")[0].strip() if not "command not found" in netagent_version
                                    else "Banyan Netagent", "Not Installed")
    
    return health_status



if __name__ == "__main__":
    my_ip, health = parse_argv()
    machine_details, machines = get_machine_details(my_ip)

    if health:
        func_output = health_check()
        print func_output
    else:
        manage(machine_details)
