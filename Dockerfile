# Use uma imagem base com Python instalado
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do projeto para dentro do contêiner
COPY . /app

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta do Streamlit (padrão 8501)
EXPOSE 8501

# Comando para rodar o aplicativo quando o contêiner iniciar
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]

