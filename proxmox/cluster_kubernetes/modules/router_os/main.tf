resource "routeros_interface_vlan" "interface_vlan" {
  interface = var.interface
  name      = var.name
  vlan_id   = var.vlan_id
}

resource "routeros_ip_address" "address" {
  depends_on = [routeros_interface_vlan.interface_vlan]
  address    = "${var.address}/${var.cidr}"
  disabled   = false
  interface  = routeros_interface_vlan.interface_vlan.name
}

