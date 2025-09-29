output "vm_id" {
  description = "ID do clone criado"
  value       = proxmox_virtual_environment_vm.clone.id
}

output "vm_name" {
  description = "Nome da VM"
  value       = proxmox_virtual_environment_vm.clone.name
}

output "vm_ipv4" {
  description = "Endereço IPv4 da VM (primeira interface)"
  value       = proxmox_virtual_environment_vm.clone.ipv4_addresses[0][0]
}

output "vm_password" {
  description = "Senha do usuário da VM"
  value       = random_password.vm_password.result
  sensitive   = true
}
