#!/bin/bash

set -e

if ! command -v python3 &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y python3 python3-venv
fi

python3 -m venv .venv
source .venv/bin/activate

pip install --upgarde pip
pip install -r requirements.txt

echo "insira as credenciais do servidor:"

read -p "→ Endereço IP do Servidor: " SERVER_IP
read -p "→ Usuario do Servidor: " USERNAME
read -s -p "→ Senha: " PASSWORD
read -p "→ Caminho para arquivos CSV: " CSV_PATH

REMOTE_PORT=${REMOTE_PORT:-1883}
LOCAL_PORT=${LOCAL_PORT:-1883}
TOPIC=${TOPIC:-devices/rasp1/data}
CLIENT_ID=${CLIENT_ID:-rasp}
BROKER=${BROKER:-localhost}
SERVER_DIR=${SERVER_DIR:-/home/csi/COLETA-TESTE}


cat <<EOF > .env
SERVER_IP=${SERVER_IP}
USERNAME=${USERNAME}
PASSWORD=${PASSWORD}
REMOTE_PORT=${REMOTE_PORT}
LOCAL_PORT=${LOCAL_PORT}
TOPIC=${TOPIC}
CLIENT_ID=${CLIENT_ID}
BROKER=${BROKER}
CSV_PATH="${CSV_PATH}"
SERVER_DIR="${SERVER_DIR}"
EOF

echo ""
echo "setup concluído"