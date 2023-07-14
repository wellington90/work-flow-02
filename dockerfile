# Use a imagem base do Python
FROM python:3.9-slim

# Instale o pacote redis-tools
RUN apt-get update && apt-get install -y redis-tools

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do aplicativo Flask para o contêiner
COPY . /app

# Instale as dependências do aplicativo
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta do aplicativo Flask
EXPOSE 5000

# Aguarde 10 sec antes de iniciar o aplicativo Flask
CMD sh -c "sleep 10 && python3 app.py"

