FROM python:3.13-slim


RUN pip3 install Flask pyOpenSSL


COPY multi_protocol_service.py /app/multi_protocol_service.py

COPY ./ssl/cert.pem /app/cert.pem
COPY ./ssl/key.pem /app/key.pem


WORKDIR /app


EXPOSE 443
EXPOSE 8080


CMD ["python", "multi_protocol_service.py"]