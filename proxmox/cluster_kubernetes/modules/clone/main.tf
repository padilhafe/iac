resource "random_password" "vm_ssh_password" {
  length           = 16
  override_special = "_%@"
  special          = true
}

# Clone da VM a partir do template
resource "proxmox_virtual_environment_vm" "clone" {
  name      = var.name
  node_name = var.node_name

  clone {
    vm_id = var.template_id
  }

  agent {
    enabled = true
  }

  cpu {
    cores = var.cpu_cores
  }

  memory {
    dedicated = var.memory_mb
  }

  initialization {
    user_data_file_id = var.cloud_init_file_id

    user_account {
      username = var.vm_ssh_username
      password = random_password.vm_ssh_password.result
      keys = var.vm_ssh_public_key != null ? [var.vm_ssh_public_key,] : null
    }
    
    ip_config {
      ipv4 {
        address = var.ip_address != null && var.ip_address != "" ? var.ip_address : "dhcp"
        gateway = var.ip_address != null && var.ip_address != "" ? var.gateway    : null
      }
    }

    dns {
      servers = var.dns_servers
    }
  }

  network_device {
    bridge  = var.bridge
    vlan_id = var.vlan_id
  }

  disk {
    size         = var.disk_size_gb
    datastore_id = var.datastore_id
    interface    = "scsi"
  }
}
