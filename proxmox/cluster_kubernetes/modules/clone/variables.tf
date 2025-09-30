variable "name" {}
variable "hostname" {}
variable "node_name" {}
variable "vm_datastore_id" {}
variable "disk_size_gb" {}
variable "template_id" {}

variable "vm_ssh_username" {
  default = "iac"
}
variable "vm_ssh_public_key" {
  type = string
  default = null
}
variable "cpu_cores" {
  default = 2
}
variable "memory_mb" {
  default = 1024
}
variable "ip_address" {
  type = string
  default = null
}
variable "gateway" {
  type = string
  default = null
}

variable "vlan_id" {
  default = 0
}
variable "bridge" {
  default = "vmbr0"
}
variable "dns_servers" {
  default = ["1.1.1.1", "8.8.8.8"]
}

variable "snippets_datastore_id" {
  description = "Datastore onde os snippets serão armazenados"
  type        = string
  default     = "snippets"
}

variable "vm_id" {
  description = "ID da VM. Se não for fornecido, será atribuído automaticamente."
  type        = number
  default     = null
}
