FROM python:3.13-slim


ENV APP_PORT=80
ENV APP_PORT=443     
ENV TCP_PORT1=8080    


WORKDIR /app


COPY multi_protocol_service.py /app/multi_protocol_service.py


COPY cert.pem /app/cert.pem
COPY key.pem /app/key.pem


RUN pip install Flask pyOpenSSL


CMD ["python", "/app/multi_protocol_service.py"]




