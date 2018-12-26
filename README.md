# Introduction to Apache Pulsar

This repository contains the code used in the demo part of my talk "Life beyond Kafka with Apache Pulsar".

## Requirements

- Git
- VirtualBox

## Deploy services

### Kubernetes cluster

The first thing to do is to install and deploy a Kubernetes cluster where we will run our Apache Pulsar cluster:
    
    # Install minikube command
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.32.0/minikube-linux-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube
    
    # Install
    curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.12.4/bin/linux/amd64/kubectl && chmod +x kubectl && sudo cp kubectl /usr/local/bin/ && rm kubectl

    # Start a minikube cluster
    minikube start --memory=8192 --cpus=4

    # Configure kubectl to use minikube
    kubectl config use-context minikube

    # Test it with an example application
    kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.4 --port=8080
    kubectl expose deployment hello-minikube --type=NodePort
    curl $(minikube service hello-minikube --url)   
    kubectl delete service hello-minikube
    kubectl delete deployment hello-minikube

    # Launch dashboard
    minikube dashboard

### Helm

In order to deploy the services in K8s, we will use Helm. So next thing is to install it:
    
    # Install helm command
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get | sh

    # Init helm
    helm init

    # Test it with an example application
    helm install stable/mysql --name mysql-test
    kubectl get pods
    helm delete stable/mysql
    helm delete edgy-kangaroo

### Apache Pulsar cluster

After a Kubernertes cluster is ready to use, the first thing to do is to deploy an Apache Puslar cluster

    # Clone Apache Pulsar repository
    git clone https://github.com/apache/pulsar.git

    # Install Pulsar chart
    cd pulsar/deployment/kubernetes/helm
    helm install --values pulsar/values-mini.yaml ./pulsar --name pulsar-cluster

    # Check Pulsar cluster
    helm status pulsar-cluster

    # Launch Pulsar Web service url
    browser http://$(minikube ip):30001/

