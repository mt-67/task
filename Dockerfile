FROM python:3.13-slim


RUN pip3 install Flask
RUN pip3 install socket
RUN pip3 install threading


COPY multi_protocol_service.py /app/app.py
COPY cert.pem /app/cert.pem
COPY key.pem /app/key.pem


WORKDIR /app


EXPOSE 443
EXPOSE 8080
EXPOSE 9000


CMD ["python", "multi_protocol_service.py"]