# CSI-MQTT

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

![Linux Badge](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=000&style=flat) [![Paho-MQTT](https://badge.fury.io/py/paho-mqtt.svg)](https://pypi.org/project/paho-mqtt/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)

Projeto em Python para transmissão de dados de sensores via Raspberry Pi usando MQTT. 

# Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Licença](#licença)

# Instalação


1. Clone o repositório:

```bash
git clone https://github.com/brunomoraes15/CSI-MQTT.git
cd CSI-MQTT.git```

2. Crie um ambiente virtual para instalar as dependências do Python:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```
---

# Configuração


1. Dentro do ambiente virtual, crie o arquivo `credentials.env`:

```bash
sudo nano venv/credentials.env
```

2. Adicione ao arquivo as seguintes configurações:

```yaml
SSH_SERVER_IP=127.0.0.1
SSH_USER=user
SSH_PASSWORD=0000
REMOTE_PORT=1883
LOCAL_PORT=1883
```

Configure de acordo com as configurações do servidor. A porta ativa padrão é 22.

3. Opcional: Ajuste o nível de logs no arquivo `logging.conf`.

---

# Execução


Execute o script `ssh_tunnel.py` para conectar ao servidor:

```bash
python -m raspberry.ssh_tunnel
```

---

# Licença


Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.