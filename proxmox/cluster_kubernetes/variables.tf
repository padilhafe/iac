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
  default     = "pve01"
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
  default     = "vm-storage"
}
