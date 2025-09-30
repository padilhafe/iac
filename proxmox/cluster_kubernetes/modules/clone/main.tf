resource "random_password" "vm_ssh_password" {
  length           = 16
  override_special = "_%@"
  special          = true
}

# Clone da VM a partir do template
resource "proxmox_virtual_environment_vm" "clone" {
  name      = var.name
  node_name = var.node_name
  vm_id     = var.vm_id != null ? var.vm_id : null

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
    user_data_file_id = proxmox_virtual_environment_file.cloud_init.id

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
    datastore_id = var.vm_datastore_id
    interface    = "virtio0"
  }
}

resource "proxmox_virtual_environment_file" "cloud_init" {
  content_type = "snippets"
  datastore_id = var.snippets_datastore_id
  node_name    = var.node_name

  source_raw {
    data = <<-EOF
      #cloud-config
      hostname: ${var.hostname}
      timezone: America/Sao_Paulo
      users:
        - name: ${var.vm_ssh_username}
          sudo: ALL=(ALL) NOPASSWD:ALL
          shell: /bin/bash
          lock_passwd: false
          passwd: ${random_password.vm_ssh_password.result}
          ssh_authorized_keys:
            - ${var.vm_ssh_public_key}
      package_update: true
      packages:
        - qemu-guest-agent
        - net-tools
        - curl
      runcmd:
        - systemctl enable qemu-guest-agent
        - systemctl start qemu-guest-agent
    EOF

    file_name = "${var.name}_cloud_init.yaml"
  }
}
