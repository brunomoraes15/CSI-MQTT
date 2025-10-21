#!/bin/bash

set -e

if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instalando..."
    sudo apt-get update && sudo apt-get install -y python3 python3-venv
fi

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Configuração do ambiente:"
read -p "→ Caminho para os arquivos CSV: " CSV_PATH

SERVER_IP="10.20.241.10"
REMOTE_PORT=1883
LOCAL_PORT=1883
TOPIC="devices/rasp1/data"
CLIENT_ID="rasp"
BROKER="localhost"
SERVER_DIR="/home/csi/COLETA-TESTE"


cat <<EOF > credentials.env
SERVER_IP=${SERVER_IP}
REMOTE_PORT=${REMOTE_PORT}
LOCAL_PORT=${LOCAL_PORT}
TOPIC=${TOPIC}
CLIENT_ID=${CLIENT_ID}
BROKER=${BROKER}
CSV_PATH="${CSV_PATH}"
SERVER_DIR="${SERVER_DIR}"
EOF

echo ""
echo "Setup concluído"
echo ""
cat credentials.env
