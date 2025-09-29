output "template_id" {
  description = "ID do template criado no Proxmox"
  value       = proxmox_virtual_environment_vm.template.id
}

output "template_name" {
  description = "Nome do template"
  value       = proxmox_virtual_environment_vm.template.name
}
