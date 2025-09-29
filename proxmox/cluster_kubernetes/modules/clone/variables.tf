variable "provider_name" {}
variable "provider_version" {}
variable "name" {}
variable "hostname" {}
variable "node_name" {}
variable "datastore_id" {}
variable "template_id" {}
variable "cloud_init_file_id" {
  description = "ID do cloud-init compartilhado"
  type        = string
}
variable "cpu_cores" {
  default = 2
}
variable "memory_mb" {
  default = 1024
}
variable "ip_address" {
  default = "dhcp"
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
