class banyan::netagent (
  $version="UNSET",
  $shield_addr="UNSET",
  $gpg_password="UNSET",
  $server_cidr="UNSET",
  $client_cidr="UNSET"
  ) {

  # sudo /opt/puppetlabs/bin/puppet module install staging
  include staging

  if ($version == "UNSET") or ($shield_addr == "UNSET") or ($gpg_password == "UNSET") {
    warning("Netagent install failed - you need to set version, shield_addr, gpg_password.")
  
  } elsif ($server_cidr != "UNSET") and ($client_cidr != "UNSET") {
    warning("Netagent install failed - you can set either server_cidr or client_cidr, but not both.")

  } else {

    $download_url = "https://www.banyanops.com/netting/netagent-${version}.tar.gz"
    $install_folder = "/opt/banyan/netagent-${version}"
    $logs_folder = "/var/log/banyan"

    if $client_cidr == "UNSET" {
      $client_cidr = ""
    }
    if $server_cidr == "UNSET" {
      $server_cidr = ""
    }

    # create dirs we use
    file { "/opt/banyan" :
      ensure => "directory"
    }
    file { "${install_folder}" :
      ensure => "directory"    
    }
    file { "${logs_folder}" :
      ensure => "directory"
    }

    # download netagent and create the config-netagent file
    staging::deploy { "netagent-${version}.tar.gz" :
      source => $download_url,
      target => "/opt/banyan",
      creates => "${install_folder}/config-netagent.tpl",
    } ->
    file { "${install_folder}/config-netagent" :
      ensure => present,
      source => "${install_folder}/config-netagent.tpl",
      replace => false,
      notify => Exec["setup_netagent"],      
    }

    file { "${install_folder}/client-cidr.txt" :
      ensure => present,
      content => "${client_cidr}",
      notify => Exec["setup_netagent"],      
    } ->
    file { "${install_folder}/server_cidr.txt" :
      ensure => present,
      content => "${server_cidr}",
      notify => Exec["setup_netagent"],      
    }

    file_line { "config-netagent__log_home" :
      path => "${install_folder}/config-netagent",
      line => "log_home=/var/log/banyan",
      match => "^log_home=.*$",
      notify => Exec["setup_netagent"],    
    }
    file_line { "config-netagent__gpg_password" :
      path => "${install_folder}/config-netagent",
      line => "gpg_password=${gpg_password}",
      match => "^gpg_password=.*$",
      notify => Exec["setup_netagent"],
    }
    file_line { "config-netagent__shield_addr" :
      path => "${install_folder}/config-netagent",
      line => "shield_addr=${shield_addr}",
      match => "^shield_addr=.*$",
      notify => Exec["setup_netagent"],    
    }

    exec { "setup_netagent" :
      command => "${install_folder}/setup-netagent.sh",
      refreshonly => true,
    }  

  }  

}
