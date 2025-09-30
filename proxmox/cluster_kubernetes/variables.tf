variable "provider_name" {
  type        = string
  description = "O provider a ser usado para Proxmox Virtual Environment"
  default     = "bpg/proxmox"
}

variable "provider_version" {
  type        = string
  description = "Versão do provider Proxmox VE"
  default     = "0.84.1"
}

variable "node_name" {
  type        = string
  description = "Nó para rodar os recursos"
  default     = "pve"
}

variable "proxmox_ve_ssh_user" {
  type        = string
  description = "Usuário SSH para conectar ao Proxmox VE"
  default     = "root"
}

variable "proxmox_ve_ssh_private_key" {
  type        = string
  description = "Caminho para a chave privada SSH"
  default     = "/home/felipepadilha/.ssh/id_ed25519"
}

variable "vm_ssh_public_key" {
  type        = string
  description = "Chave pública SSH para as VMs"
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMLko3dGIj36xzQ5tMW8qo55U0GeVGLlEaOV7/0OAwOh felipepadilha@DESKTOP-FQM9KAA\n"
}

variable "snippets_datastore_id" {
  type        = string
  description = "Datastore para Snippets"
  default     = "snippets"  
}

variable "template_datastore_id" {
  type        = string
  description = "Datastore para Templates e Imagens"
  default     = "cloud-images"
}

variable "vm_datastore_id" {
  type        = string
  description = "Datastore para VMs"
  default     = "local-lvm"
}

variable "vm_ssh_username" {
  type        = string
  description = "Nome do usuário SSH para as VMs"
  default     = "iac"
}

variable "interface" {
  type        = string
  description = "Interface física no roteador para a rede Kubernetes"
  default     = "ether6"
}

variable "interface_name" {
  type        = string
  description = "Nome da interface VLAN para a rede Kubernetes"
  default     = "VLAN90_K8S_NETWORK"
}

variable "vlan_id" {
  type        = number
  description = "ID da VLAN para a rede Kubernetes"
  default     = 90
}

variable "gateway" {
  type        = string
  description = "Gateway para a rede Kubernetes"
  default     = "10.90.90.1"
}

variable "cidr" {
  type        = number
  description = "CIDR para a rede Kubernetes"
  default     = 24
}

variable "network_prefix" {
  type        = string
  description = "Prefixo de IP para os nós do Kubernetes"
  default     = "10.90.90"
}

variable "dns_servers" {
  type        = list(string)
  description = "Servidores DNS para as VMs"
  default     = ["192.168.10.30", "8.8.8.8"]
}