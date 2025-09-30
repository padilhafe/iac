output "cloud_init_id" {
  description = "ID do arquivo cloud-init compartilhado"
  value       = proxmox_virtual_environment_file.quemu_agent.id
}

output "cloud_init_name" {
  description = "Nome do arquivo cloud-init"
  value       = proxmox_virtual_environment_file.quemu_agent.file_name
}
