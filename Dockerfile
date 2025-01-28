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

# Executa o ls novamente no diretório /app para listar o conteúdo após a cópia
RUN ls -lah /app

# Garante que a pasta /app tenha permissões de escrita
RUN chmod -R 777 /app

# Porta exposta (FastAPI padrão 8000)
EXPOSE 9500
ARG TOKEN

ENV TOKEN=$TOKEN

# Comando para rodar a aplicação com Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9500"]
