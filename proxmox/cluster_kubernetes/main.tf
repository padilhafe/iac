# ----------------------------------------
# Cloud-init fixo
# ----------------------------------------
module "cloud_init" {
  source           = "./modules/cloud_init"
  node_name        = var.node_name
  datastore_id     = var.datastore_config_id
  provider_name    = var.provider_name
  provider_version = var.provider_version
}

# ----------------------------------------
# Templates de SO
# ----------------------------------------
module "ubuntu_template" {
  provider_version = var.provider_version
  provider_name    = var.provider_name
  source           = "./modules/templates"
  node_name        = var.node_name
  datastore_id     = var.datastore_template_id
  template_name    = "ubuntu24-template"
  image_url        = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
  content_type     = "import"
  file_name         = "ubuntu-24.04.qcow2"
}

module "debian_template" {
  provider_version = var.provider_version
  provider_name    = var.provider_name
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
module "app01" {
  source             = "./modules/clone"
  name               = "app01"
  hostname           = "app01"
  vm_ssh_username    = var.vm_ssh_username
  node_name          = var.node_name
  datastore_id       = var.datastore_vm_id
  template_id        = module.ubuntu_template.template_id
  cloud_init_file_id = module.cloud_init.cloud_init_id
  memory_mb          = 2048
  vlan_id            = 30
  provider_name      = var.provider_name
  provider_version   = var.provider_version
}

module "db01" {
  source             = "./modules/clone"
  name               = "db01"
  hostname           = "db01"
  node_name          = var.node_name
  datastore_id       = var.datastore_vm_id
  template_id        = module.debian_template.template_id
  cloud_init_file_id = module.cloud_init.cloud_init_id
  memory_mb          = 4096
  vlan_id            = 30
  provider_name      = var.provider_name
  provider_version   = var.provider_version
}
