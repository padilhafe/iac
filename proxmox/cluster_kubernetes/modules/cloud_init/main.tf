resource "proxmox_virtual_environment_file" "quemu_agent" {
  content_type = "snippets"
  datastore_id = var.datastore_id
  node_name    = var.node_name

  source_raw {
    data = <<-EOF
      #cloud-config
      timezone: America/Sao_Paulo
      package_update: true
      packages:
        - qemu-guest-agent
      runcmd:
        - systemctl enable qemu-guest-agent
        - systemctl start qemu-guest-agent
    EOF

    file_name = "qemu-guest-agent.yaml"
  }
}
