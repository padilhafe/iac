resource "local_file" "ansible_inventory" {
  content = templatefile("inventory.tmpl",
    {
      master = {
        index = range(3)
        ip_address = [for m in module.masters : m.vm_ipv4]
        user = var.vm_ssh_username
        vm_name = [for m in module.masters : m.vm_name]
      }
      worker = {
        index = range(3)
        ip_address = [for w in module.workers : w.vm_ipv4]
        user = var.vm_ssh_username
        vm_name = [for w in module.workers : w.vm_name]
      }
      ssh_private_key = var.proxmox_ve_ssh_private_key
    }
  )
  filename = "inventory.yml"
  file_permission = "0600"
}