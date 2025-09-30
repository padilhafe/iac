# ----------------------------------------
# Template Ubuntu Noble Numbat
# ----------------------------------------
module "ubuntu_template" {
  source        = "./modules/templates"
  node_name     = var.node_name
  datastore_id  = var.template_datastore_id
  template_name = "ubuntu24-template"
  image_url     = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
  content_type  = "import"
  file_name     = "ubuntu-24.04.qcow2"
}


# ----------------------------------------
# Configuração do RouterOS
# ----------------------------------------
module "routeros" {
  source    = "./modules/router_os"
  interface = var.interface
  name      = var.interface_name
  vlan_id   = var.vlan_id
  address   = var.gateway
  cidr      = var.cidr
}

# ----------------------------------------
# Clones de VMs
# ----------------------------------------
module "masters" {
  count                 = 3
  source                = "./modules/clone"
  name                  = "k8s-master0${count.index + 1}"
  hostname              = "k8s-master0${count.index + 1}"
  vm_ssh_username       = var.vm_ssh_username
  vm_ssh_public_key     = var.vm_ssh_public_key
  node_name             = var.node_name
  vm_id                 = 300 + count.index + 1
  vm_datastore_id       = var.vm_datastore_id
  snippets_datastore_id = var.snippets_datastore_id
  disk_size_gb          = 20
  template_id           = module.ubuntu_template.template_id
  cpu_cores             = 2
  ip_address            = "${var.network_prefix}.2${count.index + 1}/${var.cidr}"
  gateway               = var.gateway
  memory_mb             = 4096
  vlan_id               = var.vlan_id
  dns_servers           = var.dns_servers
  depends_on            = [module.routeros]
}

module "workers" {
  count                 = 3
  source                = "./modules/clone"
  name                  = "k8s-worker0${count.index + 1}"
  hostname              = "k8s-worker0${count.index + 1}"
  vm_ssh_username       = var.vm_ssh_username
  vm_ssh_public_key     = var.vm_ssh_public_key
  node_name             = var.node_name
  vm_id                 = 400 + count.index + 1
  vm_datastore_id       = var.vm_datastore_id
  snippets_datastore_id = var.snippets_datastore_id
  disk_size_gb          = 50
  template_id           = module.ubuntu_template.template_id
  cpu_cores             = 2
  ip_address            = "${var.network_prefix}.3${count.index + 1}/${var.cidr}"
  gateway               = var.gateway
  memory_mb             = 2048
  vlan_id               = var.vlan_id
  dns_servers           = var.dns_servers
  depends_on            = [module.routeros, module.masters]
}

