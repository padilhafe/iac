.DEFAULT_GOAL := run

apply:
	@terraform apply -auto-approve

plan:
	@terraform plan

init:
	@terraform init -upgrade
	@git clone -q --branch v2.28.1 --depth 1 https://github.com/kubernetes-sigs/kubespray.git kubespray 2>/dev/null || echo "Kubespray já clonado"
	@python3 -m venv .venv
	@. .venv/bin/activate && pip install -r kubespray/requirements.txt

cluster:
	@. .venv/bin/activate && cd kubespray && ansible-playbook -i ../inventory.yml cluster.yml --become --become-user=root

destroy:
	@terraform destroy -auto-approve

ping:
	@ansible -i inventory.yml all -m ping

run: init apply cluster

.PHONY: update-provider init apply plan destroy run ping cluster