class banyan::shield (
  $shield_version="UNSET", 
  $org_id="UNSET",
  $cluster_name="cluster1",
  $shield_opts="NONE"
  
  ) {

  include staging
  include stdlib

  if ($shield_opts == "NONE") {
    $shield_opts_to_set=""
  } else {
    $shield_opts_to_set="\"${shield_opts}\""
  }

  if ($shield_version == "UNSET") or ($org_id == "UNSET") {
    warning("Not installing shield - need to set shield_version and org_id.")
  
  } else {

    # get release candidates from staging S3 instead of production S3
    if $shield_version =~ /.*-rc/ {
      $site = "www-stage.bnntest.com"
    } else {
      $site = "www.banyanops.com"
    }
    $shield_download_url = "http://${site}/netting/shield-${shield_version}.tar.gz"
    
    notice("--> Downloading Shield from ${shield_download_url}")

    $shield_folder = "/opt/banyan/shield-${shield_version}"

    ensure_resource("file", ["/opt/banyan", "${shield_folder}", "/var/log/banyan"], {"ensure" => "directory"})
    
    staging::deploy { "shield-${shield_version}.tar.gz" :
      source => $shield_download_url,
      target => "/opt/banyan",
      creates => "${shield_folder}/config-shield.tpl",    
    } ->
    file { "${shield_folder}/config-shield" :
      ensure => present,
      source => "${shield_folder}/config-shield.tpl",
      replace => false,      
      notify => Exec["setup_shield"],      
    }

    file_line { "config-shield__log_home" :
      path => "${shield_folder}/config-shield",
      line => "log_home=/var/log/banyan",
      match => "^log_home=.*$",
      notify => Exec["setup_shield"],
    }
    file_line { "config-shield__org_id" :
      path => "${shield_folder}/config-shield",
      line => "org_id=${org_id}",
      match => "^org_id=.*$",
      notify => Exec["setup_shield"],
    }
    file_line { "config-shield__cluster_name" :
      path => "${shield_folder}/config-shield",
      line => "cluster_name=${cluster_name}",
      match => "^cluster_name=.*$",
      notify => Exec["setup_shield"],
    }  
    file_line { "config-shield__shield_opts" :
      path => "${shield_folder}/config-shield",
      line => "shield_opts=${shield_opts_to_set}",
      match => "^shield_opts=.*$",
      notify => Exec["setup_shield"],
    }

    exec { "setup_shield" :
      command => "${shield_folder}/setup-shield.sh",
      refreshonly => true,
    }
  }
}
