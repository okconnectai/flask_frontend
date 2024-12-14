#!/bin/bash

# Diretório do projeto
cd /var/www/html/app

# Adicionar todas as mudanças
git add .

# Commit com mensagem e timestamp
git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"

# Pull para garantir que estamos atualizados
git pull origin main

# Push das alterações
git push origin main

# Reiniciar o serviço Flask (opcional)
# sudo systemctl restart flask_app
