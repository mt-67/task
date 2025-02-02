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

First, I created a Flask application « multi-protocol-service.py » in Python that will listen to HTTP/HTTPS/TCP ports (80, 443, 8080) and outputs « Hello, Noda » on 20.103.44.21 and https://192.168.1.32:443 and http://192.168.1.32:80

Flash works via HTTP by default, so to add HTTPS support to Flash, you need to configure self-signed SSL certificates, key.pem and cert.pem, Self-signed SSL certificates need to encrypt traffic without using commercial certificates.

```Bash
openssl x509 -req -in csr.pem -signkey key.pem -out cert.pem -days 365 
```
It will be valid for 365 days.


# Create, Building and Launch Dockerfile/DockerImage

To deploy this service in Kubernetes, we will package it in a Docker container named ports-service. To do this, I created a Dockerfile.

Using the official Python image

```Bash
FROM python:3.13-slim
```
Mappins ports 

```Bash
EXPOSE 80
EXPOSE 443
EXPOSE 8080
```
and Launching the Flask application

```Bash
CMD ["python", "multi-protocol-service.py"]
```

Building a Docker image

```Bash
docker build -t ports-service
```

After the build, you can start the container with ports open (80, 443, 8080)

```Bash
docker run -p 80:80 -p 443:443 -p 8080:8080 ports-service
```


# Working with Azure AKS

Using Azure CLI,log in to my account.

Сreate a cluster. I chose the westeurope region by taking 3 nodes to distribute the load, and if one node falls, the other two will be able to share its load, and generate-ssh-keys,ssh keys are needed for node management and access to the Master node. 

```Bash
az aks create --resource-group <myResourceGroup> --name <myAKSCluster> --node-count 3 --enable-addons monitoring --generate-ssh-keys
```

To connect to the cluster, you need to get credentials for AKS and configure kubectl.

```Bash
az aks get-credentials --resource-group <resource-group-name> --name <aks-cluster-name>
```

I checked the connection using « kubectl get nodes » 

I have set up policy and given myself an « Owner »  for full access to all actions.


# Manifestos
