# 🚀 Jenkins CI/CD Pipeline for GKE Guess Number App

Hi! I’m excited to share my journey of setting up a complete CI/CD pipeline using Jenkins, Google Kubernetes Engine (GKE), and AWS EC2. The pipeline pulls code from my [guess-number-app GitHub repository](https://github.com/nagrohan579/guess-number-app.git), builds a Docker image, pushes it to Docker Hub, and deploys it to a Kubernetes cluster on GCP.

---

## 📦 Project Overview

- **GitHub Repo Used:** [guess-number-app](https://github.com/nagrohan579/guess-number-app.git)
- **Jenkins runs on:** AWS EC2 (Ubuntu 24.04)
- **Kubernetes Cluster:** Google Kubernetes Engine (GKE)
- **CI/CD:** Jenkins Pipeline

---

## 🛠️ Step 1: Setting Up GCP Project & GKE Cluster

I started by creating a new GCP project:

![Create GCP Project](images/gcp_create_new_project.png)

Then, I enabled the Kubernetes Engine API:

![Enable Kubernetes Engine API](images/gcp_enable_kubernetes_engine_api.png)

Navigated to the Kubernetes Engine Clusters page:

![Kubernetes Engine Clusters](images/gcp_kubernetes_engine_clusters_page.png)

Clicked "Create" and chose the Autopilot cluster option:

![Create Autopilot Cluster](images/gcp_create_autopilot_cluster.png)

But I needed a standard cluster, so I switched:

![Create Standard Cluster](images/gcp_create_a_kubernetes_cluster.png)

### My Cluster Configuration

- **Cluster Name:** gke-guess-number-game
- **Location Type:** Zonal (us-central1-c)
- **Release Channel:** Rapid
- **Kubernetes Version:** 1.33.1-gke.1386000
- **Machine Type:** N1 g1-small (1 vCPU, 1.7 GB RAM)
- **Boot Disk:** 32 GB
- **Autoscaler:** Disabled
- **Cloud Logging/Monitoring:** Enabled for system components

Cluster created successfully!

![Cluster Created](images/gcp_kubernetes_cluster_created.png)

By default, it had 3 nodes. I only needed one, so I edited the node pool:

![Edit Node Pool](images/gcp_edit_node_pool.png)
![Cluster Updated to 1 Node](images/gcp_kubernetes_cluster_updated_to_1_node.png)

---

## 🔐 Step 2: Service Account for Jenkins

I created a dedicated service account for CI/CD deployments:

![Creating Service Account](images/gcp_creating_new_service_account.png)

**Details:**
- **Name:** guess-number-deployer
- **Role:** Kubernetes Engine Developer (least privilege principle)
- **Email:** guess-number-deployer@gke-guess-number-app.iam.gserviceaccount.com

![Service Account Created](images/gcp_service_account_created.png)

Generated a new key for Jenkins:

![New Service Account Key](images/gcp_new_service_account_key_created.png)

---

## ☁️ Step 3: Provisioning Jenkins on AWS EC2

I spun up an EC2 instance:

- **AMI:** Ubuntu 24.04
- **Type:** t2.medium
- **Storage:** 30 GiB
- **Security Group:** Custom TCP 8080 open to 0.0.0.0/0

![Creating EC2 Instance](images/aws_creating_new_ec2_instance.png)
![EC2 Instance Created](images/aws_ec2_instance_created.png)
![Editing Inbound Rules](images/aws_ec2_security_group_editing_inbound_rules.png)

Connected via SSH:

![Connecting to EC2 via SSH](images/aws_connecting_to_ec2_via_ssh.png)

---

## ⚙️ Jenkins Installation

I updated packages and followed the [official Jenkins instructions](https://pkg.jenkins.io/):

```bash
sudo apt update
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install fontconfig openjdk-17-jre
sudo apt-get install jenkins
```

Started Jenkins:

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

Checked status:

```bash
sudo systemctl status jenkins
```

---

## 🌐 Jenkins Web UI Setup

Accessed Jenkins at `http://<EC2_PUBLIC_IP>:8080`:

![Jenkins Getting Started](images/jenkins_getting_started_page.png)

Got the admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Installed suggested plugins:

![Select Plugins](images/jenkins_select_plugin_install_option.png)

Created the first admin user:

![Create Admin User](images/jenkins_create_first_admin_user_account.png)

Landed on the Jenkins welcome page:

![Jenkins Welcome](images/jenkins_welcome_page.png)

---

## 🔌 Jenkins Plugins & Credentials

Installed **Pipeline: Stage View**:

![Add Stage View Plugin](images/jenkins_add_stage_view_plugin.png)

Added DockerHub credentials:

![Add DockerHub Credentials](images/jenkins_add_docker_hub_credentials.png)
![DockerHub Credentials Created](images/jenkins_dockerhub_credentials_created.png)

Installed these plugins:
- Docker
- Docker Pipeline
- Kubernetes
- Kubernetes CLI

Added GCP service account key as a secret credential (`gcloud-creds`).

---

## 🏗️ Jenkins Pipeline Job

Created a new Pipeline job:

![Creating New Job](images/jenkins_creating_new_job.png)

Configured it to pull from my [GitHub repo](https://github.com/nagrohan579/guess-number-app.git), branch `main`.

Triggered a build—after some troubleshooting, it succeeded!

![Pipeline Build Successful](images/jenkins_pipeline_build_successful.png)

---

## ☸️ Verifying Deployment on GKE

Connected to the GKE cluster, checked pods and services:

```bash
kubectl get pods
kubectl get svc
```

![Pods and Services Running](images/gcp_kubernetes_pods_and_services_running.png)

Copied the external IP, visited in browser—my app was live!

![App Running in Browser](images/app_running_in_browser.png)

---

## 🐞 Issues I Faced

1. **Quota Issues:** Had to switch to a zonal cluster and adjust node count/machine type.
2. **Service Account Permissions:** Ensured least-privilege by using "Kubernetes Engine Developer".
3. **withKubeConfig & KubernetesEngineBuilder:** Spent a lot of time, but these approaches didn’t work due to `kubectl` issues.
4. **Solution:** Installed `gcloud` CLI and the GKE auth plugin on Jenkins EC2, which worked perfectly.

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates gnupg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install -y google-cloud-sdk
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```

---

## 📝 Jenkinsfile Explained

Here’s the Jenkinsfile I used:

```groovy
pipeline {
  agent any

  environment {
    dockerimagename = "rohannagcalsoft/guess-number-app"
    PROJECT_ID      = 'gke-guess-number-app'
    CLUSTER_NAME    = 'gke-guess-number-game'
    LOCATION        = 'us-central1-c'
    GCLOUD_CREDS    = credentials('gcloud-creds')   
    DOCKER_CREDS    = 'dockerhub-credentials'       
    NAMESPACE       = 'default'
  }

  stages {
    stage('Maven Build') {
      steps {
        sh 'mvn clean package'
      }
    }

    stage('Build image') {
      steps {
        script {
          dockerImage = docker.build(dockerimagename)
        }
      }
    }

    stage('Pushing Image') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDS) {
            dockerImage.push("latest")
          }
        }
      }
    }

    stage('Deploying App to Kubernetes') {
      steps {
        script {
          // Activate service account using the injected JSON file
          sh """
            gcloud auth activate-service-account --key-file=$GCLOUD_CREDS
            gcloud config set project $PROJECT_ID
            gcloud config set compute/zone $LOCATION
          """

          // Get cluster credentials locally (sets up kubectl config)
          sh "gcloud container clusters get-credentials $CLUSTER_NAME --zone $LOCATION --project $PROJECT_ID"

          // Ensure kubectl is present 
          sh 'curl -LO "https://dl.k8s.io/release/v1.20.5/bin/linux/amd64/kubectl"'
          sh 'chmod u+x kubectl'

          // Deploy app manifests
          sh './kubectl apply -f k8s/'
        }
      }
    }
  }
}
```

### What Each Stage Does

- **Maven Build:**  
  I run `mvn clean package` to build the Java app and create the JAR file.

- **Build image:**  
  I use Jenkins’ Docker plugin to build a Docker image tagged as `rohannagcalsoft/guess-number-app:latest`.

- **Pushing Image:**  
  I log in to Docker Hub using my stored credentials and push the image.

- **Deploying App to Kubernetes:**  
  - I activate my GCP service account using the injected JSON key.
  - I set the GCP project and zone.
  - I fetch cluster credentials so `kubectl` can talk to my GKE cluster.
  - I download `kubectl` if it’s not present.
  - I apply all Kubernetes manifests from the `k8s/` directory to deploy the app.


