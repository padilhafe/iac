#!/bin/bash
set -e

cd "$(dirname "$0")/.."

# Extrai o bloco terraform do provider principal
terraform_block=$(sed -n '/^terraform {/,/^}$/p' provider.tf)

# Atualiza (sobrescreve) o provider.tf em todos os módulos
for module_dir in modules/*/; do
    if [ -d "$module_dir" ]; then
        module_provider="$module_dir/provider.tf"

        # Sobrescreve sem dó nem piedade
        echo "$terraform_block" > "$module_provider"
        echo "Provider sobrescrito em $module_dir"
    fi
done

echo "Todos os arquivos do Provider foram sobrescritos com sucesso."
