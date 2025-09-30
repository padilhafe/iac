terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "0.84.1"
    }
    routeros = {
      source = "terraform-routeros/routeros"
      version = "1.88.0"
    }
  }
}

provider "proxmox" {
  insecure = true
  ssh {
    agent = true
    username = var.proxmox_ve_ssh_user
    private_key = file(var.proxmox_ve_ssh_private_key)
  }
}

provider "routeros" {
  insecure = true
}