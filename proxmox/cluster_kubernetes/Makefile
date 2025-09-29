.DEFAULT_GOAL := apply

apply:
	terraform apply -auto-approve

plan:
	terraform plan

init:
	terraform init -upgrade

destroy:
	terraform destroy -auto-approve

env:
    @export PROXMOX_VE_ENDPOINT="https://endereco-do-seu-proxmox:8006/"
	@export PROXMOX_VE_API_TOKEN="terraform-prov@pve!terraform-token:TOKEN"
    @export PROXMOX_VE_SSH_USER="seu-usuario"
	@export PROXMOX_VE_SSH_PRIVATE_KEY="caminho/para/sua/chave"
	@export PROXMOX_VE_TLS_INSECURE="true"
	@echo "Variáveis de ambiente para o Proxmox VE configuradas."

.PHONY: apply plan init destroy env