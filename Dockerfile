# Dockerfile

FROM python:3.9-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para /app
COPY ./src /app/src

# Porta exposta (FastAPI padrão 8000)
EXPOSE 9000

# Comando para rodar a aplicação com Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9000"]
