# Dockerfile configurado com instruções claras 
#O projeto utiliza um Dockerfile para criar a imagem da aplicação ServiceDesk Cloud API. 
#Esse arquivo define o ambiente de execução da API, instala as dependências, copia o código-fonte, configura permissões, expõe a porta da aplicação e executa o servidor Uvicorn.


FROM python:3.12-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]