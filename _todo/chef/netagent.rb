
version = "UNSET" unless (node["banyan"] && node["banyan"]["netagent"]["version"])
shield_addr = "UNSET" unless (node["banyan"] && node["banyan"]["netagent"]["shield_addr"])
gpg_password = "UNSET" unless (node["banyan"] && node["banyan"]["netagent"]["gpg_password"])
server_cidr = "UNSET" unless (node["banyan"] && node["banyan"]["netagent"]["server_cidr"])
client_cidr = "UNSET" unless (node["banyan"] && node["banyan"]["netagent"]["client_cidr"])

if ((version == "UNSET") || (shield_addr == "UNSET") || (gpg_password == "UNSET"))
  log "msg" do
    message "Netagent install failed - you need to set version, shield_addr, gpg_password."
    level :warn
  end
  return

elsif ((server_cidr != "UNSET") && (client_cidr != "UNSET"))
  log "msg" do
    message "Netagent install failed - you can set either server_cidr or client_cidr, but not both."
    level :warn
  end
  return  

else

  download_url = "https://www.banyanops.com/netting/netagent-#{version}.tar.gz"
  install_folder = "/opt/banyan/netagent-#{version}"
  logs_folder = "/var/log/banyan"

  if (client_cidr == "UNSET")
    client_cidr = ""
  end
  if (server_cidr == "UNSET")
    server_cidr = ""
  end  

  # create dirs we use
  directory "/opt/banyan" do
    action :create
  end
  directory install_folder do
    action :create
  end
  directory logs_folder do
    action :create
  end

  # download netagent and create the config-netagent file
  remote_file "/opt/banyan/netagent-#{version}.tar.gz" do
    source download_url
    action :create
  end
  execute "untar-banyan" do
    command "tar zxvf netagent-#{version}.tar.gz"
    cwd '/opt/banyan'
    not_if { File.exists?("#{install_folder}/config-netagent.tpl")}
  end  
  remote_file "#{install_folder}/config-netagent" do
    source "file://#{install_folder}/config-netagent.tpl"
    action :create
  end  

  file "#{install_folder}/client-cidr.txt" do
    content "#{client_cidr}"
    action :create
    notifies :run, "execute[setup-netagent]", :immediate
  end
  file "#{install_folder}/server-cidr.txt" do
    content "#{server_cidr}"
    action :create
    notifies :run, "execute[setup-netagent]", :immediate
  end

  ruby_block "config-netagent" do
    block do
      sed = Chef::Util::FileEdit.new("#{install_folder}/config-netagent")
      sed.search_file_replace(/^log_home=.*$/, "log_home=/var/log/banyan")
      sed.search_file_replace(/^gpg_password=.*$/, "gpg_password=#{gpg_password}")
      sed.search_file_replace(/^shield_addr=.*$/, "shield_addr=#{shield_addr}")
      sed.write_file
    end
    notifies :run, "execute[setup-netagent]", :immediate
  end

  execute "setup-netagent" do
    command "#{install_folder}/setup-netagent.sh"
    action :nothing
  end

end