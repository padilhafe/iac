# Baixa a imagem do SO
resource "proxmox_virtual_environment_download_file" "image" {
  content_type = var.content_type
  datastore_id = var.datastore_id
  node_name    = var.node_name
  url          = var.image_url
  file_name    = var.file_name
}

# Cria o template base
resource "proxmox_virtual_environment_vm" "template" {
  name      = var.template_name
  node_name = var.node_name

  template  = true
  started   = false

  cpu {
    cores = var.cpu_cores
  }

  memory {
    dedicated = var.memory_mb
  }

  disk {
    datastore_id = var.datastore_id
    import_from  = proxmox_virtual_environment_download_file.image.id
    interface    = "virtio0"
    iothread     = true
    discard      = "on"
    size         = var.disk_size
  }

  initialization {
    ip_config {
      ipv4 {
        address = "dhcp"
      }
    }
  }
}
