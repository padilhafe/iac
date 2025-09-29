output "app01_ip" { value = module.app01.vm_ipv4 }
output "app01_id" { value = module.app01.vm_id }
output "app01_password" { 
  value = module.app01.vm_ssh_password
  sensitive = true
}

output "db01_ip"  { value = module.db01.vm_ipv4 }
output "db01_id"  { value = module.db01.vm_id }
output "db01_password" { 
  value = module.db01.vm_ssh_password
  sensitive = true
}
