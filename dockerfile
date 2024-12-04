# Use uma imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]