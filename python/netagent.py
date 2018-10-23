""" Install Banyan Netagent """

import argparse
import os
import re


def download_binary(args):
  download_url = "https://www.banyanops.com/netting/" 
  netagent_tarball = "netagent-" + args.install_version + ".tar.gz"
  
  print "--> Installing %s from %s" % (netagent_tarball, download_url)

  if os.path.isfile(netagent_tarball):
    print "--> Tarball already downloaded."
    return True

  os.system("wget " + download_url + netagent_tarball)
  os.system("tar zxf " + netagent_tarball)

  return True


def update_config(args):
  netagent_folder = "netagent-" + args.install_version
  netagent_config = netagent_folder + "/config-netagent"
  netagent_cidrs = netagent_folder + "/cidrs.txt"
  netagent_services = netagent_folder + "/services.json"

  arg_services = args.services_file is not None
  arg_cidrs = args.cidrs_file is not None
  
  print "--> Updating config file %s" % netagent_config

  os.system("cp %s.tpl %s" % (netagent_config, netagent_config))

  with open(netagent_config, "r+") as f:
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in lines:
      line = re.sub(r'shield_addr=.*', 'shield_addr=%s' % args.shield_address, line)
      line = re.sub(r'gpg_password=.*', 'gpg_password=%s' % args.gpg_password, line)
      line = re.sub(r'one_time_key=.*', 'one_time_key=%s' % args.one_time_key, line)
      line = re.sub(r'netagent_tags=.*', 'netagent_tags=%s' % args.netagent_tags, line)
      if arg_services:
        line = re.sub(r'services_from_file=.*', 'services_from_file=true', line)
      if arg_cidrs:
        line = re.sub(r'visibility_only=.*', 'visibility_only=false', line)
      f.write(line)

  if arg_services:
    with open(netagent_services, "w+") as f:
      f.write(args.services_file.read())

  if arg_cidrs:
    with open(netagent_cidrs, "w+") as f:
      f.write(args.cidrs_file.read())

  return True


def run_setup(args):
  netagent_folder = "netagent-" + args.install_version  
  netagent_setup = netagent_folder + "/setup-netagent.sh"
  print "--> Running netagent setup %s" % netagent_setup

  os.system("./%s" % netagent_setup)

  return True



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--install-version', required=True, help="Netagent version to install")
  parser.add_argument('--shield-address', required=True, help="Shield address as ADDR:PORT to connect to")
  parser.add_argument('--gpg-password', required=True, help="GPG password (available from Banyan)")
  parser.add_argument('--one-time-key', required=True, help="One Time Key (available from Banyan)")
  parser.add_argument('--netagent-tags', required=True, help="Metadata labels applied to all containers/processes on the host")
  parser.add_argument('--cidrs-file', type=argparse.FileType('r'), help="Path to cidrs.txt")
  parser.add_argument('--services-file', type=argparse.FileType('r'), help="Path to services.json")

  arguments = parser.parse_args()

  download_binary(arguments)

  update_config(arguments)

  run_setup(arguments)
