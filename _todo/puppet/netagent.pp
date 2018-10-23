class banyan::netagent (
  $netagent_version="UNSET",
  $shield_addr="UNSET",
  $disable_docker="true",
  $disable_L7="false"
  ) {

  include staging
  include stdlib

  if ($netagent_version == "UNSET") or ($shield_addr == "UNSET") {
    warning("Not installing netagent - need to set netagent_version and shield_addr.")
  
  } else {

    # get release candidates from staging S3 instead of production S3
    if $netagent_version =~ /.*-rc/ {
      $site = "www-stage.bnntest.com"
    } else {
      $site = "www.banyanops.com"
    }
    $netagent_download_url = "http://${site}/netting/netagent-${netagent_version}.tar.gz"
    $kernelmod_download_url = "http://${site}/netting/kms/${netagent_version}/${::kernelrelease}/netting.gpg"
    
    notice("--> Downloading Netagent from ${netagent_download_url}")

    $netagent_folder = "/opt/banyan/netagent-${netagent_version}"
    $kernelmod_folder = "/opt/banyan/netagent-${netagent_version}/${::kernelrelease}"

    ensure_resource("file", ["/opt/banyan", "${netagent_folder}", "${kernelmod_folder}", "/var/log/banyan"], {"ensure" => "directory"})

    staging::deploy { "netagent-${netagent_version}.tar.gz" :
      source => $netagent_download_url,
      target => "/opt/banyan",
      creates => "${netagent_folder}/config-netagent.tpl",
    } ->
    file { "${netagent_folder}/config-netagent" :
      ensure => present,
      source => "${netagent_folder}/config-netagent.tpl",
      replace => false,
      notify => Exec["setup_netagent"],      
    }

    file_line { "config-netagent__log_home" :
      path => "${netagent_folder}/config-netagent",
      line => "log_home=/var/log/banyan",
      match => "^log_home=.*$",
      notify => Exec["setup_netagent"],    
    }
    file_line { "config-netagent__gpg_password" :
      path => "${netagent_folder}/config-netagent",
      line => "gpg_password=gobany@n",
      match => "^gpg_password=.*$",
      notify => Exec["setup_netagent"],
    }
    file_line { "config-netagent__shield_addr" :
      path => "${netagent_folder}/config-netagent",
      line => "shield_addr=${shield_addr}",
      match => "^shield_addr=.*$",
      notify => Exec["setup_netagent"],    
    }
    file_line { "config-netagent__disable_docker" :
      path => "${netagent_folder}/config-netagent",
      line => "disable_docker=${disable_docker}",
      match => "^disable_docker=.*$",
      notify => Exec["setup_netagent"],    
    }
    file_line { "config-netagent__disable_L7" :
      path => "${netagent_folder}/config-netagent",
      line => "disable_L7=${disable_L7}",
      match => "^disable_L7=.*$",
      notify => Exec["setup_netagent"],    
    }

    staging::file { "${::kernelrelease}/netting.gpg" :
      source => $kernelmod_download_url,
      target => "${kernelmod_folder}/netting.gpg"
    } ->
    file { "${netagent_folder}/netting-location" :
      ensure => present,
      content => "${kernelmod_folder}",
      notify => Exec["setup_netagent"],      
    }

    exec { "setup_netagent" :
      command => "${netagent_folder}/setup-netagent.sh",
      refreshonly => true,
    }  

  }  

}
