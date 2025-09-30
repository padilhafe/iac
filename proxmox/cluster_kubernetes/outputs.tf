output "master_ips" {
  description = "Endereços IP de todos os nós master"
  value       = [for m in module.masters : m.vm_ipv4]
}

output "master_passwords" {
  description = "Senhas de todos os nós master"
  value       = [for m in module.masters : m.vm_ssh_password]
  sensitive   = true
}

output "worker_ips" {
  description = "Endereços IP de todos os nós worker"
  value       = [for m in module.workers : m.vm_ipv4]
}

output "worker_passwords" {
  description = "Senhas de todos os nós worker"
  value       = [for m in module.workers : m.vm_ssh_password]
  sensitive   = true
}

