# Banyan Netagent configuration

# GPG password (available from Banyan)
gpg_password:

# Shield address as IP_ADDR:PORT
shield_address:
# Listen TCP port on localhost
listen_port: 9999

# Set to true if Shield requires secure bootstrapping
secure_bootstrap: true
# One Time Key to register Netagent, mandatory if Shield requires secure bootstrapping (available from Banyan Dashboard)
one_time_key:

# Label all processes/containers on the host with custom metadata (list of key:value pairs)
host_tags:
    ostype: linux 
    k8s: true

# Visibility mode (ignore CIDRs, roles, policies)
visibility_only: true
# Source of public IP info: AWS, GCE, default, none
public_ip_source: default
# Disable L7 protocol parsing
disable_layer_7: true
# Traffic to ignore, as list of executable commands
ignore_traffic:
    - consul
    - etcd
    - haproxy

# Deploy netagent in elastic access tier
access_tier: false
# Provide client address transparency
address_transparency: true

# Lifetime of a certificate
cert_lifetime: 24h

# Read service specifications from a file
services_from_file: false

# Filename for service specifications
services_file_name: /opt/banyan/services.json

# Max percentage usage of each CPU core [1-100]
cpu_limit: 100

# Console log level: ERR,WARN,INFO,DEBUG
console_log_level: ERR
# File log level: ERR,WARN,INFO,DEBUG
file_log_level: INFO

# **************************************************************/
# *** The most commonly modified options are above this line ***/
# **************************************************************/

# ****************** shield ********************/

# If Shield goes down for this long then policies switch to permissive
# shield_timeout: 10m

# ****************** proxy *********************/

# access event credit-based rate limiting
# access_event_credits_limiting: true
# access_event_credits_max: 1000
# access_event_credits_interval: 1m
# access_event_credits_per_interval: 1

# access event rate limiting by derived event key [key = source address + user + ...]
# access_event_key_limiting: true
# access_event_key_expiration: 9m

# TCP keepalive
# keep_alive: true
# Idle time before sending TCP keepalive
# keep_idle: 59s
# Time between consecutive TCP keepalives
# keep_interval: 59s
# Keepalive missing ACKs before closing connection
# keep_count: 3

# Client identification timeout
# client_timeout: 20s

# Forwarding gateway mode, e.g., VPN
# forward: false
# List of ingress CIDRs for forwarding gateway mode, e.g., VPN
# forward_ingress: []

# ****************** netagent ******************/

# Turn on CPU profiling by giving prof output filepath
# cpu_profile:
# Turn on memory profiling
# mem_profile: false

# Log output to LOGFILENAME
# file_log: true
# Number of log files (auto-rotations)
# log_num: 10
# Max size of each log file in megabytes
# log_size: 50
# Number of kafka log files (auto-rotations)
# kafka_log_num: 2
# Max size of each kafka log file in megabytes
# kafka_log_size: 50

# Use the kernel module (true) or not (false)
# kernel: true
# Host-only mode
# host_only: true
# Disable monitoring Docker
# disable_docker: false

# Send all-zero data points to Shield
# send_zeros: false
# Statistics reporting interval [secs]
# period: 20

# Enable request level access events
# request_level_events: true

# ************* keypair ************************/

# Use RSA instead of ECDSA
# use_rsa: false

# ***************** http *********************/

# Perform OIDC redirects only if HTTP request host matches domain name in service spec
# oidc_strict_host: false

# ****************** k8s ***********************/

# Access Kubernetes kubelet for pod info
kubelet: true
# Kubernetes kubelet addr:port
kubelet_addr: http://localhost:10255
# Use Istio
#istio: false
# Address to access Istio data
# istio_address: 
# Address to listen for Istio authz requests
# istio_auth_listen: localhost:9990
