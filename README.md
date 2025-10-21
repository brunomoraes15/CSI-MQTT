


# CSI-MQTT

[![made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![Linux Badge](https://img.shields.io/badge/Linux-FCC624?logo=linux\&logoColor=000\&style=flat)
[![Paho-MQTT](https://badge.fury.io/py/paho-mqtt.svg)](https://pypi.org/project/paho-mqtt/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**CSI-MQTT** é um projeto em Python para transmissão de dados de sensores conectados a um **Raspberry Pi** para um servidor remoto via **MQTT**.

---

## Índice

* [Pré-requisitos](#pré-requisitos)
* [Instalação](#instalação)
* [Configuração](#configuração)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Execução](#execução)
* [Logs e Monitoramento](#logs-e-monitoramento)
* [Execução Automática com systemd](#execução-automática-com-systemd)
* [Licença](#licença)

---

## Pré-requisitos

Antes de iniciar, verifique se você possui:

* **Raspberry Pi** (qualquer modelo compatível com Python 3)
* **Python 3.13+**
* **Pip** atualizado
* **MQTT Broker** instalado no servidor (ex.: Mosquitto)
* Conexão de rede entre Raspberry Pi e servidor

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/brunomoraes15/CSI-MQTT.git
cd CSI-MQTT
```

2. Execute o script de instalação:

```bash
chmod u+x install.sh
./install.sh
```


---

## Configuração

O projeto utiliza um arquivo `credentials.env` para armazenar as credenciais de conexão MQTT e os diretórios de trabalho.
### `credentials.env`

```env
SERVER_IP=192.168.0.0
REMOTE_PORT=1883
LOCAL_PORT=1883
BROKER=localhost
CLIENT_ID=rasp
TOPIC=devices/rasp1/data
CSV_PATH="/home/user/folder"
SERVER_DIR="/home/user-user/"
```

### Parâmetros

| Variável        | Descrição                                                            |
| --------------- | -------------------------------------------------------------------- |
| **SERVER_IP**   | Endereço IP do servidor MQTT ou da máquina que hospeda o broker.     |
| **REMOTE_PORT** | Porta usada para comunicação com o broker remoto (padrão: `1883`).   |
| **LOCAL_PORT**  | Porta usada localmente para testes com o broker em `localhost`.      |
| **BROKER**      | Hostname ou IP do broker MQTT (ex.: `localhost` para uso local).     |
| **CLIENT_ID**   | Identificador único do cliente MQTT (ex.: `rasp`, `rasp2`, etc.).    |
| **TOPIC**       | Tópico MQTT onde as mensagens serão publicadas ou recebidas.         |
| **CSV_PATH**    | Caminho local onde os arquivos `.csv` de sensores estão armazenados. |
| **SERVER_DIR**  | Diretório remoto de destino (usado para upload ou sincronização).    |


---

## Estrutura do Projeto

```
CSI-MQTT/
│
├─ raspberry/      
│   └─ rasp.py
│   └─ publisher.py
│
├─ server/         
│   └─ server.py
│   └─ broker.py
│
├─ general/         
│   └─ logging.py
│
├─ credentials.env  # Configurações de acesso MQTT
├─ install.sh       # Script de instalação
├─ requirements.txt # Dependências
└─ LICENSE
```

---

## Execução

### No Raspberry Pi

```bash
python3 -m raspberry.rasp
```

* O script **verifica os CSVs disponíveis** e envia sequencialmente para o servidor via MQTT.

### No Servidor

```bash
python3 -m server.server
```

* Recebe os dados enviados pelo Pi e registra logs detalhados.

---

## Logs e Monitoramento

O projeto gera logs em:

```
general/logs/mqtt.log
```

* Inclui **informações de envio, erros de conexão e status do broker**.

---

## Execução Automática com systemd (Raspberry Pi)

Para rodar o script automaticamente no boot:

1. Crie um arquivo de serviço:

```bash
sudo nano /etc/systemd/system/csi-mqtt.service
```

2. Cole o seguinte:

```ini
[Unit]
Description=CSI-MQTT Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/CSI-MQTT
ExecStart=/usr/bin/python3 -m raspberry.rasp
Restart=always
EnvironmentFile=/home/pi/CSI-MQTT/credentials.env

[Install]
WantedBy=multi-user.target
```

3. Ative o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable csi-mqtt.service
sudo systemctl start csi-mqtt.service
```

* Para monitorar logs:

```bash
sudo journalctl -u csi-mqtt.service -f
```

---

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

