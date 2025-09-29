#!/bin/bash
set -e

cd "$(dirname "$0")/.."

outputs=$(terraform output | awk '{print $1}')

hosts=$(echo "$outputs" | awk -F'_' '{print $1}' | sort -u)

for host in $hosts; do
    echo "=== ${host} ==="

    for var in $(echo "$outputs" | grep "^${host}_"); do
        value=$(terraform output -raw "$var")
        echo "$var: $value"
    done
    echo
done
