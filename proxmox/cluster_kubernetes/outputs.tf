# Cloud-init
output "cloud_init_id" {
  value = module.ubuntu_base_cloud_init.cloud_init_id
}

# VMs
output "app01_ip" { value = module.app01.vm_ipv4 }
output "app01_id" { value = module.app01.vm_id }
output "db01_ip"  { value = module.db01.vm_ipv4 }
output "db01_id"  { value = module.db01.vm_id }
