variable "provider_name" {}
variable "provider_version" {}

variable "node_name" {
  description = "Node Proxmox onde o template será criado"
  type        = string
}

variable "content_type" {
  description = "Tipo de conteúdo da imagem (iso, qcow2, etc.)"
  type        = string
  default     = null
}

variable "file_name" {
  type        = string
  description = "Nome do arquivo salvo no datastore, com extensão correta (.qcow2, .raw, etc)"
}

variable "datastore_id" {
  description = "Datastore onde a imagem/template será armazenado"
  type        = string
}

variable "template_name" {
  description = "Nome do template a ser criado"
  type        = string
}

variable "image_url" {
  description = "URL da imagem do SO (Ubuntu, Debian, etc.)"
  type        = string
}

variable "cpu_cores" {
  description = "Número de cores para o template"
  type        = number
  default     = 2
}

variable "memory_mb" {
  description = "Quantidade de memória para o template em MB"
  type        = number
  default     = 2048
}

variable "disk_size" {
  description = "Tamanho do disco do template em GB"
  type        = number
  default     = 8
}
