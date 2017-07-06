""" This is a module for netagent installation"""

import os
import sys
import json
import re

from time import strftime, localtime, time

GPG_PASSWORD = "gobany@n"

def install_netagent(machine_details):

    netagent_version = "netagent-" + machine_details["netagent"]
    netagent_role = machine_details.get("netagent_role", "client")
    netagent_logging = machine_details.get("netagent_logging", "ERR")
    NETAGENT_OPTS = "--cloglevel=%s --floglevel=%s" % ('ERR', netagent_logging)

    download_url = "https://www.banyanops.com/netting/" 
    if "-rc" in netagent_version:
        download_url = "https://www-stage.bnntest.com/netting/"

    os.system("echo '==> Starting Netagent installation, version: %s from: %s'" % (netagent_version, download_url))

    NETAGENT_INSTALL_COMMANDS = [
        "sudo apt-get update -qq",
        "wget " + download_url + netagent_version + ".tar.gz",
        "sleep 10",
        "tar zxvf " + netagent_version + ".tar.gz",
        "sleep 10"
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
            elif re.search(r'netagent_opts=', line):
                line = line.replace('=', '="' + NETAGENT_OPTS + '"')
            f.write(line)
    
    # Client on Mesos nodes
    if netagent_role == "client":
        for i in range(len(NETAGENT_SERVER_LIST)):
            os.system('echo ' + NETAGENT_SERVER_LIST[i] + ' --dport 9092 >> client-cidr.txt')

    if netagent_role == "server":
        os.system('echo ' + CURRENT_NODE + ' --dport 9092 >> server-cidr.txt')
 
    os.system('./setup-netagent.sh')
    os.chdir(cwd)

    netagent_data = {
        "Netagent_Version": netagent_version,
        "Netagent_Role": netagent_role,
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
            os.system("echo '==> Netagent installed'")
        else:
            stop_netagent()
            start_netagent()
            os.system("echo '==> Netagent installed, correct version, restarting'")
    else:
        stop_netagent()
        os.system("echo '==> Netagent stopped / not installed '")          



if __name__ == "__main__":
    machine_details, machines = get_machine_details(CURRENT_NODE)
    manage(machine_details)
