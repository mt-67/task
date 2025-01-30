FROM python:3.13-slim


RUN pip3 install Flask pyOpenSSL


COPY multi_protocol_service.py /main/main.py
COPY cert.pem /main/cert.pem
COPY key.pem /main/key.pem


WORKDIR /main


EXPOSE 443
EXPOSE 8080


CMD ["python", "multi_protocol_service.py"]