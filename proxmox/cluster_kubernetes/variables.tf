variable "provider_name" {
  type        = string
  description = "O provider a ser usado para Proxmox Virtual Environment"
  default     = "bpg/proxmox"
}

variable "provider_version" {
  type        = string
  description = "Versão do provider Proxmox VE"
  default     = "0.84.1"
}

variable "node_name" {
  type        = string
  description = "Nó para rodar os recursos"
  default     = "pve"
}

variable "proxmox_ve_ssh_user" {
  type        = string
  description = "Usuário SSH para conectar ao Proxmox VE"
  default     = "root"
}

variable "proxmox_ve_ssh_private_key" {
  type        = string
  description = "Caminho para a chave privada SSH"
  default     = "/home/felipepadilha/.ssh/id_ed25519"
}

variable "datastore_config_id" {
  type        = string
  description = "Datastore para Snippets"
  default     = "snippets"  
}

variable "datastore_template_id" {
  type        = string
  description = "Datastore para Templates e Imagens"
  default     = "cloud-images"
}

variable "datastore_vm_id" {
  type        = string
  description = "Datastore para VMs"
  default     = "local-lvm"
}

variable "vm_ssh_username" {
  type        = string
  description = "Nome do usuário SSH para as VMs"
  default     = "iac"
}
