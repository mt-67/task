# Multi-Port Service Deployment with Kubernetes and Azure DevOps Pipeline

The project is the development and automation of the deployment of a service that listens to HTTP, HTTPS, and custom TCP ports. We have created a Python application using Flask for HTTP/HTTPS and the socket standard library for TCP. The application is packaged in a Docker container, which allows it to be deployed to Kubernetes in Azure ACR. The process includes creating manifests for Kubernetes, configuring the Helm chart to simplify deployment, and integrating with Azure DevOps to automatically deploy and test services.


# Purpose

Develop and deploy a service that will listen to HTTP, HTTPS, and custom TCP ports using Python (Flask for HTTP/HTTPS and sockets for TCP). The service is packaged in a Docker container and deployed to Kybernetes using a Helm chart, providing automation through Azure DevOps for CI/CD pipelines. The project also implemented the deployment success check and rollback of the release in case of errors, which ensures stable operation of services in Kubernetes.


# Content

- [Multi-Port Service Deployment with Kubernetes and Azure DevOps Pipeline](#Multi-Port_Service_Deployment_with_Kubernetes_and_Azure_DevOps_Pipeline)
- [Purpose](#Purpose)
- [Content](#Content)
- [Technologies](#Technologies)
- [Instruction](#Instruction)
- [The project team](#The_project_team)


# Technologies

- [Python](#Python)
- [Flask framework](#Flask_framework)
- [Docker](#Docker)
- [Kubernetes](#Kubernetes)
- [Azure CR](#Azure_CR)
- [Azure KS](#Azure_KS)
- [Azure DevOps](#Azure_DevOps)
- [Helm-chart](#Helm-chart)


# Instruction

# Create Multi-Port Service

First, I created a Flask application in Python that will listen to HTTP/HTTPS/TCP ports (80, 443, 8080).

Flash works via HTTP by default, so to add HTTPS support to Flash, you need to configure self-signed SSL certificates, key.pem and cert.pem, using the command.

```Bash
openssl x509 -req -in csr.pem -signkey key.pem -out cert.pem -days 365 
```
It will be valid for 365 days.
