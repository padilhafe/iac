# ----------------------------------------
# Cloud-init fixo
# ----------------------------------------
module "cloud_init" {
  source           = "./modules/cloud_init"
  node_name        = var.node_name
  datastore_id     = var.datastore_config_id
}

# ----------------------------------------
# Templates de SO
# ----------------------------------------
module "debian_template" {
  source           = "./modules/templates"
  node_name        = var.node_name
  datastore_id     = var.datastore_template_id
  template_name    = "debian13-template"
  image_url        = "https://cloud.debian.org/images/cloud/trixie/latest/debian-13-genericcloud-amd64.qcow2"
  content_type     = "import"
  file_name         = "debian-13.qcow2"
}

# ----------------------------------------
# Clones de VMs
# ----------------------------------------
module "masters" {
  count              = 3
  source             = "./modules/clone"
  name               = "k8s-master0${count.index + 1}"
  hostname           = "k8s-master0${count.index + 1}"
  vm_ssh_username    = var.vm_ssh_username
  node_name          = var.node_name
  datastore_id       = var.datastore_vm_id
  disk_size_gb       = 20
  template_id        = module.debian_template.template_id
  cloud_init_file_id = module.cloud_init.cloud_init_id
  cpu_cores          = 2
  ip_address        = "10.30.30.2${count.index + 1}/24"
  gateway           = "10.30.30.1"
  memory_mb          = 4096
  vlan_id            = 30
  dns_servers        = ["192.168.10.30", "8.8.8.8"]
}

module "workers" {
  count              = 3
  source             = "./modules/clone"
  name               = "k8s-worker0${count.index + 1}"
  hostname           = "k8s-worker0${count.index + 1}"
  vm_ssh_username    = var.vm_ssh_username
  node_name          = var.node_name
  datastore_id       = var.datastore_vm_id
  disk_size_gb       = 50
  template_id        = module.debian_template.template_id
  cloud_init_file_id = module.cloud_init.cloud_init_id
  cpu_cores          = 2
  ip_address        = "10.30.30.3${count.index + 1}/24"
  gateway           = "10.30.30.1"
  memory_mb          = 2048
  vlan_id            = 30
  dns_servers        = ["192.168.10.30", "8.8.8.8"]
}

