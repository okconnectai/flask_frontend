# Use uma imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Defina a variável de ambiente FLASK_ENV como development
ENV FLASK_ENV=development

# Comando para rodar a aplicação
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]