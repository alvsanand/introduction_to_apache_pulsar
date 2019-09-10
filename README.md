# Introduction to Apache Pulsar

This repository contains the code used in the demo part of my talk "Life beyond Kafka with Apache Pulsar".

## Requirements

- Git
- VirtualBox

## Deploy services

### Kubernetes cluster

The first thing to do is to install and deploy a Kubernetes cluster where we will run our Apache Pulsar cluster:

    # Install minikube command
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube

    # Install
    curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && chmod +x kubectl && sudo cp kubectl /usr/local/bin/ && rm kubectl

    # Start a minikube cluster
    minikube start --memory=12288 --cpus=8

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
    helm delete mysql-test

### Apache Pulsar cluster

After a Kubernertes cluster is ready to use, the first thing to do is to deploy an Apache Puslar cluster

    # Clone Apache Pulsar repository
    git clone https://github.com/apache/pulsar.git && cd pulsar

    # Check stable version
    git checkout tags/v2.4.1


    # Install Pulsar chart
    cd deployment/kubernetes/helm
    helm install --values pulsar/values-mini.yaml ./pulsar --name pulsar-cluster

    # Check Pulsar cluster
    watch helm status pulsar-cluster

    # Forward Pulsar dashboard port
    kubectl port-forward --namespace pulsar $(kubectl get pods --namespace pulsar -l component=dashboard -o jsonpath='{.items[*].metadata.name}') 8081:80 > /dev/null 2>&1 &

    # Launch Pulsar dashboard
    xdg-open http://localhost:8081

    # In case Dashboard does not show any cluster, delete Pulsar dashboard pod
    kubectl delete pods --namespace pulsar $(kubectl get pods --namespace pulsar -l component=dashboard -o jsonpath='{.items[*].metadata.name}')

    # Forward Pulsar Grafana port
    kubectl port-forward --namespace pulsar $(kubectl get pods --namespace pulsar -l component=grafana -o jsonpath='{.items[*].metadata.name}') 23000:3000 > /dev/null 2>&1 &

    # Launch Pulsar Grafana
    xdg-open http://localhost:23000

    # Forward Pulsar Prometheus port
    kubectl port-forward --namespace pulsar $(kubectl get pods --namespace pulsar -l component=prometheus -o jsonpath='{.items[*].metadata.name}') 29090:9090 > /dev/null 2>&1 &

    # Launch Pulsar Prometheus
    xdg-open http://localhost:29090

    # Create pulsar-admin and pulsar-perf alias
    alias pulsar-admin='kubectl exec --namespace pulsar $(kubectl get pods --namespace pulsar -l app=pulsar,component=bastion -o jsonpath={.items..metadata.name}) -it -- bin/pulsar-admin'
    alias pulsar-perf='kubectl exec --namespace pulsar $(kubectl get pods --namespace pulsar -l app=pulsar,component=bastion -o jsonpath={.items..metadata.name}) -it -- bin/pulsar-perf'

    # Create a namespace

    # Set cluster to the namespace
    pulsar-admin namespaces set-clusters public/ns1 --clusters pulsar-cluster

    # Create a test consumer
    pulsar-perf consume persistent://public/ns1/topic1

    # Create a test producer in other window
    pulsar-perf produce persistent://public/ns1/topic1

## Launch sample applications

### Python Producer

In order to generate data, we will launch a python producer that generates random transactions and send it to a Pulsar topic.

- Locally:

        cd py-producer

        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python producer.py

- Kubernetes:

        cd py-producer

        # Build IMAGE
        eval $(minikube docker-env)
        docker build -t py-producer .

        # Launch producer in K8s
        kubectl create -f deployment.yaml

        # Stop producer in K8s
        kubectl delete -f deployment.yaml

        # Create a test consumer
        pulsar-perf consume persistent://public/ns1/bank_transactions

### Function

Next to do, it is to deploy a Pulsar function that will route the transactions to different topics based on the currency:

    cd functions

    alias pulsar-admin='kubectl exec --namespace pulsar $(kubectl get pods --namespace pulsar -l app=pulsar,component=bastion -o jsonpath={.items..metadata.name}) -it -- bin/pulsar-admin'

    # Upload files to pulsar-admin pod
    for f in transaction_routing.*; do
        kubectl cp $f pulsar/$(kubectl get pods --namespace pulsar -l app=pulsar,component=bastion -o jsonpath={.items..metadata.name}):/pulsar
    done

    # Install function
    pulsar-admin functions create --functionConfigFile transaction_routing.yaml

    # Get the status of the function
    pulsar-admin functions getstatus --name transaction_routing --namespace ns1 --tenant public

    # Execute python consumer
    kubectl exec $(kubectl get pods -l app=py-producer -o jsonpath={.items..metadata.name}) -it -- bash
    export TOPIC_NAME=bank_transactions_routed_dollar
    python receiver.py
