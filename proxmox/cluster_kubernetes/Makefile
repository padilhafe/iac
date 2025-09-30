.DEFAULT_GOAL := run

apply:
	@terraform apply -auto-approve

plan:
	@terraform plan

init:
	@terraform init -upgrade

destroy:
	@terraform destroy -auto-approve

ping:
	@ansible -i inventory.yml all -m ping

run: update-provider init apply

.PHONY: update-provider init apply plan destroy run