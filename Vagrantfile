# -*- mode: ruby -*-
# vi: set ft=ruby :

# Launch a single machine:
#   vagrant up netagent-ubuntu-14.04
#
# Or, use regex to bring up groups of machines:
#   vagrant up /netagent-ubuntu.*/
#

require "yaml"
$machines = YAML.load_file(File.dirname(__FILE__) + "/machines.yml")

$provisioner = ENV["PROVISIONER"] || "python"

MEMORY=512
NUM_CPUS=1

Vagrant.configure(2) do |config|

  config.vm.provider "virtualbox" do |v|
    v.memory = MEMORY
    v.cpus   = NUM_CPUS
  end

  $machines.each do |machine|
    machine_name = machine["name"]

    config.vm.define machine_name, autostart: false do |host|
      host.vm.host_name = machine_name

      # base images from https://app.vagrantup.com
      host.vm.box = machine["box"]
      host.vm.box_check_update = false

      # vagrant automatically shares the host git repo folder at /vagrant
      # host.vm.synced_folder ".", "/vagrant"

      if $provisioner == "ansible"
        host.vm.provision "ansible" do |ansible|
          ansible.compatibility_mode = "2.0"
          ansible.playbook = "ansible-playbook-example/playbook.yml"
          ansible.become = true
        end
      else  # default is python
        host.vm.provision "shell" do |shell|
          shell.inline = "sudo /usr/bin/python /vagrant/python/netagent.py"
        end
      end

    end
  
  end

end