#!/bin/bash

# Função para verificar se o encaminhamento de porta está ativo
function check_port_forwarding {
    local port=$1
    local result=$(lsof -i :$port | grep LISTEN)
    if [[ -n $result ]]; then
        return 0
    else
        return 1
    fi
}

# Função para reiniciar o encaminhamento de porta
function restart_port_forwarding {
    local namespace=$1
    local service=$2
    local local_port=$3
    local remote_port=$4
    kubectl port-forward -n $namespace service/$service $local_port:$remote_port &
}

# Port forward Grafana
restart_port_forwarding "monitoring" "grafana" 3000 3000

# Port forward Prometheus
restart_port_forwarding "monitoring" "prometheus" 9090 9090

# Port forward my-svc
restart_port_forwarding "default" "my-svc" 5000 5000

# Aguardar até que os encaminhamentos de porta estejam ativos
sleep 5

# Verificar e reiniciar encaminhamentos de porta se necessário
while true; do
    if ! check_port_forwarding 3000; then  # Verifica se o encaminhamento de porta 3000 está ativo
        restart_port_forwarding "monitoring" "grafana" 3000 3000  # Reinicia o encaminhamento de porta para "grafana" na porta 3000
    fi

    if ! check_port_forwarding 9090; then  # Verifica se o encaminhamento de porta 9090 está ativo
        restart_port_forwarding "monitoring" "prometheus" 9090 9090  # Reinicia o encaminhamento de porta para "prometheus" na porta 9090
    fi

    if ! check_port_forwarding 5000; then  # Verifica se o encaminhamento de porta 5000 está ativo
        restart_port_forwarding "default" "my-svc" 5000 5000  # Reinicia o encaminhamento de porta para "my-svc" na porta 5000
    fi

    sleep 1  # Aguarda 1 segundo antes de verificar novamente
done
