""" Install Banyan Netagent """

import os
import re

BOOLEAN_TRUE = ["yes", "YES", "true", "True", "TRUE"]

def download_binary(params):
  download_url = "https://www.banyanops.com/netting/" 
  netagent_tarball = "netagent-" + params["install_version"] + ".tar.gz"
  
  print("--> Installing %s from %s" % (netagent_tarball, download_url))

  if os.path.isfile(netagent_tarball):
    print("--> Tarball already downloaded.")
    return True

  os.system("wget -q " + download_url + netagent_tarball)
  os.system("tar zxf " + netagent_tarball)

  return True


def update_config(params):
  netagent_folder = "netagent-" + params["install_version"]
  netagent_config = netagent_folder + "/config-netagent"

  print("--> Creating config file %s" % netagent_config)
  os.system("cp %s.tpl %s" % (netagent_config, netagent_config))

  print("--> Updating config file %s" % netagent_config)
  with open(netagent_config, "r+") as f:
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in lines:
      line = re.sub(r'shield_addr=.*', 'shield_addr=%s' % params["shield_addr"], line)
      line = re.sub(r'gpg_password=.*', 'gpg_password=%s' % params["gpg_password"], line)
      line = re.sub(r'one_time_key=.*', 'one_time_key=%s' % params["one_time_key"], line)
      line = re.sub(r'netagent_tags=.*', 'netagent_tags=%s' % params["netagent_tags"], line)
      if params["services_file"] in BOOLEAN_TRUE:
        line = re.sub(r'services_from_file=.*', 'services_from_file=true', line)
      if params["cidrs_file"] in BOOLEAN_TRUE:
        line = re.sub(r'visibility_only=.*', 'visibility_only=false', line)
      f.write(line)

  return True


def copy_files(params):
  netagent_folder = "netagent-" + params["install_version"]
  netagent_services = netagent_folder + "/services.json"
  netagent_cidrs = netagent_folder + "/cidrs.txt"

  filepath = os.path.dirname(os.path.realpath(__file__))
  services_file = filepath + "/files/services.json"
  cidrs_file = filepath + "/files/cidrs.txt"

  if params["services_file"] in BOOLEAN_TRUE:
    print("--> Copying over services file to %s" % netagent_services)
    os.system("cp %s %s" % (services_file, netagent_services))

  if params["cidrs_file"] in BOOLEAN_TRUE:
    print("--> Copying over cidrs file to %s" % netagent_cidrs)
    os.system("cp %s %s" % (cidrs_file, netagent_cidrs))

  return True


def run_setup(params):
  netagent_folder = "netagent-" + params["install_version"]
  netagent_setup = netagent_folder + "/setup-netagent.sh"
  print("--> Running netagent setup script %s" % netagent_setup)

  resp = os.system("./%s" % netagent_setup)

  return (resp == 0)



if __name__ == '__main__':

  # poor man's CONF parser so we don't need any python dependencies
  filepath = os.path.dirname(os.path.realpath(__file__))
  varsfile = filepath + "/vars.conf"
  all_vars = {}
  try:
    with open(varsfile, "r") as f:
      lines = f.readlines()
      for line in lines:
        # omit comments
        if line[0] != "#":
          elems = line.split('=', 1)
          # lines with variable: value
          if len(elems) == 2:
            elems[0] = elems[0].strip()
            elems[1] = elems[1].strip()
            # assign variable=value
            all_vars[elems[0]] = elems[1]
          else:
            raise Exception("Not in the format, variable=value - " + line)            
  except Exception as e:
    print("--> ERROR! couldn't parse variables ... please check %s" % varsfile)
    print(e)
    exit(1)

  # place installer files in user's home directory
  installer_dir = "/usr/local/banyan"
  os.system("mkdir -p %s" % installer_dir)
  os.chdir(installer_dir)  
  print("--> Installer files placed in directory: %s" % installer_dir)

  # donwload, configure, copy
  download_binary(all_vars)
  update_config(all_vars)
  copy_files(all_vars)
  
  # run setup
  if not run_setup(all_vars):
    print("--> ERROR! setup script failed ... please check logs")
  else:
    print("--> SUCCESS! setup complete")



