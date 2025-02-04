# Multi-Port Service Deployment with Kubernetes and Azure DevOps Pipeline

The project is the development and automation of the deployment of a service that listens to HTTP, HTTPS, and custom TCP ports. We have created a Python application using Flask for HTTP/HTTPS and the socket standard library for TCP. The application is packaged in a Docker container, which allows it to be deployed to Kubernetes in Azure ACR. The process includes creating manifests for Kubernetes, configuring the Helm chart to simplify deployment, and integrating with Azure DevOps to automatically deploy and test services.


# Links

my DNS http://protocolservices.westeurope.azurecontainer.io 

Flask application « multi-protocol-service.py » in Python-script that will listen to HTTP/HTTPS/TCP ports (80, 443, 8080) and outputs « Hello, Noda » on ip http://108.141.128.223 and 20.103.44.21


# Purpose

Develop and deploy a service that will listen to HTTP, HTTPS, and custom TCP ports using Python (Flask for HTTP/HTTPS and sockets for TCP). The service is packaged in a Docker container and deployed to Kybernetes using a Helm chart, providing automation through Azure DevOps for CI/CD pipelines. The project also implemented the deployment success check and rollback of the release in case of errors, which ensures stable operation of services in Kubernetes.


# Content

- [Multi-Port Service Deployment with Kubernetes and Azure DevOps Pipeline](#Multi-Port_Service_Deployment_with_Kubernetes_and_Azure_DevOps_Pipeline)
- [Links](#Links)
- [Purpose](#Purpose)
- [Content](#Content)
- [Technologies](#Technologies)
- [Instruction](#Instruction)
- [Conducted Performance Tests](#Conducted-Performance-Tests)
- [The project Team](#The_project_team)


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

First, I created a Flask application « multi-protocol-service.py » in Python that will listen to HTTP/HTTPS/TCP ports (80, 443, 8080) and outputs « Hello, Noda » on ip http://108.141.128.223 and 20.103.44.21 

Flash works through HTTP by default, so to add HTTPS support to Flash, you need to configure self-signed SSL certificates, key.pem and cert.pem, Self-signed SSL certificates need to encrypt traffic without using commercial certificates.

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

I have written YAML files to manage Kybernetes. I wrote a Deployment file to determine the number of pos, port forwarding inside the container. 

I wrote Service file to provide access to the application via ports, load balancing LoadBalancer between pods, to access the service thought an external IP, and scalability.  

I wrote an Ingress file for routing data inside the cluster via protocols to the service and ngress-nginx-controller.
Created a Secret for storing confidential data, and created DNS-name  http://protocolservices.westeurope.azurecontainer.io 

I have applied these manifests to the cluster

```Bash
kubectl apply -f <name-Manifestos>
```

and checked the status of the resources

```Bash
kubectl get <name-Manifestos-or-pods>
```


# Helm-chart

I created a Helm chart to package Kubernetes manifests for deployment automation and configuration management.

Helm simplifies the deployment of applications in Kubernetes, automates updates, and manages configuration settings via values.yaml

I created Helm-chart

```Bash
helm create relis-my-service
```

Replaced static values in the Helm chart with deployment.yml , service.yaml and ingress.yaml for my template variables.


I checked the correctness

```Bash
helm list relis-my-service
```

Launched a test rendering of the manifests

```Bash
helm template relis-my-service
```

Installed the Helm chart in the kubernetes cluster

```Bash
helm install relis-my-service ./
```

Checked the status

```Bash
helm list
```

To make changes, I am updating the expanded release.

```Bash
helm upgrade relis-my-service ./
```


# Azure DevOps Pipelines/Check Deployment, Status Deploy Helm release, available ports and unsuccessful roll up


 I signed up with a subscription, connected the container registry and Kubernetes cluster. 

 
1. I also made an Azure Pipelines « azure-pipelines-check-ports.yml » which only checks the availability of ports using Python script « only-check-ports.py »

link to the pipeline with automatic port availability check
https://dev.azure.com/matvey090/pipeline%20helm/_build?definitionId=2


2. I made the pipeline interact with Azure kubernetes and automatically deploy to kubernetes via Helm and check ports when pushing or committing to the github repository and rollback if necessary.

Created « azure-pipelines-helm-deploy-and-check.yml » in this file, I additionally activated a Python script « accessibility-rollback.py »  that checks the availability of ports and Status Deploy Helm release , if necessary, Rollback 

This file describes the steps for the CI/CD pipeline and performs a port availability test in Azure DevOps.

link to a pipeline with automatic verification of deployment, ports, and rollback, if necessary 
https://dev.azure.com/matvey090/pipeline%20helm/_build?definitionId=1


3. I wrote the wrong error deployment files on « error-deployment.yaml » and « error-values.yaml » for artificially unsuccessful rolls ups

I made an Pipeline « azure-pipelines-error-and-success.yml » that makes successful and unsuccessful rolls and runs a Python script for verification « check-error-and-rollback.py »

link to a pipeline with automatic successful and unsuccessful roll-up
https://dev.azure.com/matvey090/pipeline%20helm/_build?definitionId=3


# Python-script Check

I created a Python script that automatically checks the success of the service deployment after deployment « check-error-and-rollback.py » 

I have created a Python script that automatically checks the availability of ports and, if necessary, Rollback « accessibility-rollback.py »

I  created a Python script that automatically checks only the availability of ports « only-check-ports.py »


# Conducted Terformance Tests

Tests have been conducted, and all the elements of the assignment are functioning perfectly.

All ports are available. All the manifests and Helm-chart are successfully implemented in Kubernetes and are functioning. 

All the necessary python scripts are successfully running and working. All the Nodes, pods, and container successfully exist, work, and distribute the load.  All the necessary Azure services are working successfully. 

All Pipelines are successfully functioning and fulfilling their task. All the necessary YAML files have been written, implemented, and are functioning successfully.


# The project Team

- Matsvei Asipenka
