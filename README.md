# Installer

This repo provides tools and instruction for deploying banyan

To use the examples in this repo you will need `Ansible`, `Vagrant` and a Virtual Machine provider such as `Fusion`, `Workstation` or `VirtualBox` installed on your local system.

## Examples

Deploy with Ansible:
```
vagrant up
cd ./ansible
./ansible-playbook -i ./vagrant_inventory ./netagent_playbook.yml
```