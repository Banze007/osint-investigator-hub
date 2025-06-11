#!/bin/bash

# Ativar o ambiente virtual (não funciona diretamente no systemd, usaremos o caminho absoluto)
# source /home/kali/osint_backup/venv/bin/activate

# Navegar até o diretório do projeto
cd /home/kali/osint_backup

# Iniciar o servidor Flask usando o ambiente virtual diretamente
/home/kali/osint_backup/venv/bin/python3 /home/kali/osint_backup/venv/bin/flask run --host=0.0.0.0 --port=5000
