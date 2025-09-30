#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "=== CREDENCIAIS DO CLUSTER KUBERNETES ==="
echo

# Função para exibir credenciais de um grupo de nós
show_credentials() {
    local node_type=$1
    local ip_output="${node_type}_ips"
    local password_output="${node_type}_passwords"
    
    echo "=== ${node_type} NODES ==="
    
    # Obtém os IPs e senhas
    ips=$(terraform output -json "$ip_output" | jq -r '.[]')
    passwords=$(terraform output -json "$password_output" | jq -r '.[]')
    
    # Converte em arrays
    ip_array=($ips)
    password_array=($passwords)
    
    # Exibe as credenciais de cada nó
    for i in "${!ip_array[@]}"; do
        node_name="k8s-${node_type}0$((i+1))"
        echo "Node: $node_name"
        echo "  IP: ${ip_array[$i]}"
        echo "  User: $(terraform output -raw vm_ssh_username 2>/dev/null || echo 'iac')"
        echo "  Password: ${password_array[$i]}"
        echo
    done
}

# Verifica se jq está instalado
if ! command -v jq &> /dev/null; then
    echo "Erro: jq não está instalado. Por favor, instale jq para executar este script."
    echo "macOS: brew install jq"
    echo "Ubuntu/Debian: sudo apt install jq"
    exit 1
fi

# Exibe credenciais dos masters
show_credentials "master"

# Exibe credenciais dos workers  
show_credentials "worker"
