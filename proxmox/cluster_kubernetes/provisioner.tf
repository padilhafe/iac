resource "null_resource" "ansible" {
  # Dependências - aguarda a criação do inventário e das VMs
  depends_on = [
    local_file.ansible_inventory,
    module.masters,
    module.workers
  ]

  # Provisioner para testar conectividade com ping do Ansible
  provisioner "local-exec" {
    command = <<EOT
echo "Executa o Ansible no cluster Kubernetes..."
ansible all -i inventory.yml -m ping 
EOT
  }

  # Triggers para reexecutar quando as VMs mudarem
  triggers = {
    master_ips = join(",", [for m in module.masters : m.vm_ipv4])
    worker_ips = join(",", [for w in module.workers : w.vm_ipv4])
    inventory_content = local_file.ansible_inventory.content
  }
}
