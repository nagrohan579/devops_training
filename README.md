# DevOps Training

This repository is dedicated to tracking my journey through DevOps training at Calsoft. It serves as a collection of topics, insights, and hands-on projects as I progress through various phases of learning.

---

## 📜 Contents

1. [Part 1: Foundations of DevOps and Cloud Computing - Week 1-2](#part-1-foundations-of-devops-and-cloud-computing---week-1-2)
   - [What is DevOps?](#what-is-devops)
     - [🌟 Introduction to DevOps and Its Impact](#-introduction-to-devops-and-its-impact)
     - [🎨 Emma’s Story – Real-world Analogy](#-emmas-story--real-world-analogy)
     - [🧱 Software Development Lifecycle (SDLC)](#-software-development-lifecycle-sdlc)
     - [🔄 Software Development Models](#-software-development-models)
     - [⚠️ Challenges with Agile SDLC – Developer vs. Operations](#%EF%B8%8F-challenges-with-agile-sdlc--developer-vs-operations)
     - [🚧 Wall Between Dev and Ops](#-wall-between-dev-and-ops)
     - [🚀 Introduction to DevOps](#-introduction-to-devops)
     - [🔧 DevOps in Action – Breaking the Wall](#-devops-in-action--breaking-the-wall)
     - [🛠️ DevOps Lifecycle – Fully Automated Flow](#%EF%B8%8F-devops-lifecycle--fully-automated-flow)
   - [DevOps Principles, Practices, and Culture](#devops-principles-practices-and-culture)
     - [🧭 DevOps Principles](#-devops-principles)
     - [🛠️ DevOps Practices](#%EF%B8%8F-devops-practices)
     - [🌱 DevOps Culture](#-devops-culture)
   - [The DevOps Lifecycle](#the-devops-lifecycle)
     - [Plan](#plan)
     - [Build](#build)
     - [Test](#test)
     - [Release](#release)
     - [Deploy](#deploy)
     - [Monitor](#monitor)
     - [Operate](#operate)
   - [Assignment: Setup Helloworld Simple Jenkins CI-CD on Local Setup](Helloworld_Jenkins_CI_CD_local_setup.md)
   - [Docker – Detailed Notes](#docker--detailed-notes)
     - [Why was Docker Needed?](#why-was-docker-needed)
     - [How Docker Helped](#how-docker-helped)
     - [What are Containers?](#what-are-containers)
     - [Revisiting Operating System Concepts](#revisiting-operating-system-concepts)
     - [Containers vs Virtual Machines (VMs)](#containers-vs-virtual-machines-vms)
     - [How Applications are Deployed with Docker](#how-applications-are-deployed-with-docker)
     - [Images vs Containers](#images-vs-containers)
     - [Docker's Role in DevOps](#dockers-role-in-devops)
     - [Docker Installation Guide](#docker-installation-guide)
     - [Basic Docker Commands](#basic-docker-commands)
     - [Docker Run in Detail](#docker-run-in-detail)
    - [Dockerizing a Simple Python Flask Application](#dockerizing-a-simple-python-flask-application)
      - [Manual Deployment Steps](#manual-deployment-steps)
      - [Dockerizing the Application](#dockerizing-the-application)
      - [Build and Run the Docker Image](#build-and-run-the-docker-image)
      - [Pushing the Docker Image to Docker Hub](#pushing-the-docker-image-to-docker-hub)
      - [Conclusion](#conclusion)
    - [Environment Variables in Docker](#environment-variables-in-docker)
    - [Commands, Arguments, and Entrypoints in Docker](#commands-arguments-and-entrypoints-in-docker)
        - [Understanding Container Lifecycle](#understanding-container-lifecycle)
        - [CMD Instruction](#cmd-instruction)
        - [ENTRYPOINT Instruction](#entrypoint-instruction)
        - [Overriding ENTRYPOINT at runtime](#overriding-entrypoint-at-runtime)
        - [Important Dockerfile Summary](#important-dockerfile-summary)
    - [Docker Compose](#docker-compose)
        - [Docker Basics Recap](#-docker-basics-recap)
        - [Sample Voting Application Stack (Used Throughout the Course)](#-sample-voting-application-stack-used-throughout-the-course)
            - [Components](#components)
            - [Data Flow](#data-flow)
        - [Running Each Service via docker run](#-running-each-service-via-docker-run)
        - [Container Communication Using --link (Deprecated)](#-container-communication-using---link-deprecated)
        - [Docker Compose File (Basic Structure)](#️-docker-compose-file-basic-structure)
        - [Key Docker Compose Concepts](#-key-docker-compose-concepts)
        - [Build vs Pull](#-build-vs-pull)
        - [Networking Differences](#-networking-differences)
        - [Docker Compose Versions Summary](#-docker-compose-versions-summary)
        - [Voting App Architecture](#-voting-app-architecture)
        - [Repository Structure](#-repository-structure)
        - [Flow of Data](#-flow-of-data)
        - [Step-by-Step Deployment (Manual Docker)](#-step-by-step-deployment-manual-docker)
            - [Clone Repo](#1️⃣-clone-repo)
            - [Deploy redis (Detached)](#2️⃣-deploy-redis-detached)
            - [Build & Run vote App](#3️⃣-build--run-vote-app)
            - [Deploy postgres (Named db, Detached)](#4️⃣-deploy-postgres-named-db-detached)
            - [Build & Run worker App](#5️⃣-build--run-worker-app)
            - [Build & Run result App](#6️⃣-build--run-result-app)
        - [Containers Summary (docker ps)](#-containers-summary-docker-ps)
        - [Troubleshooting Tips](#-troubleshooting-tips)
        - [Continuation: Running Voting App with Docker Compose](#-continuation-running-voting-app-with-docker-compose)
        - [docker-compose.yml file](#️-docker-composeyml-file)
        - [Explanation of what's happening](#-explanation-of-whats-happening)
        - [How to run](#-how-to-run)
        - [Access the Voting Application](#-access-the-voting-application)
        - [Summary of this step](#-summary-of-this-step)
    - [Assignment: Use Docker to containerize an application and demo](docker-assignment/README.md)


---

## Part 1: Foundations of DevOps and Cloud Computing - Week 1-2

### What is DevOps?

#### 🌟 Introduction to DevOps and Its Impact

**Key Idea:**  
DevOps transforms the speed and efficiency of software delivery, turning tasks that took **hours or days** into ones completed in **minutes**.

**Explanation:**  
Traditionally, software development and deployment involved **siloed teams**, lengthy processes, and significant delays. DevOps introduces a **culture and set of practices** that unite development and operations, allowing companies to deliver updates faster and more reliably. This agility allows businesses to **focus more on their products and services**, which is why it's being rapidly adopted across industries.

---

#### 🎨 Emma’s Story – Real-world Analogy

**Scenario:**  
Emma, an artist who owns a physical art gallery, wants to **expand online** through a mobile app.

**What She Needs:**
- A team of **developers** to build the app.
- **Testers** to ensure its quality.
- **Operations/admins** to host and maintain the app on servers.

**Explanation:**  
Emma's situation mirrors many modern businesses that wish to digitize their services. Since she doesn’t have a technical team, she partners with a software firm. Through her journey, we explore the **real-life application of DevOps principles** in a typical software development cycle.

---

#### 🧱 Software Development Lifecycle (SDLC)

**Phases of SDLC:**

1. **Requirement Gathering & Analysis**  
   - Understanding what features the product should have.
   - How users will interact with it.
   - Research on market demand and competitive landscape.

2. **Planning**  
   - Estimating **cost**, **time**, and **resources** needed.
   - Identifying potential **risks**.

3. **Designing**  
   - Architects create technical blueprints and roadmaps for development.
   - These design documents guide developers in the coding phase.

4. **Development**  
   - Developers begin writing the actual software code.
   - This is often the most exciting and creative phase for devs.

5. **Testing**  
   - The software is thoroughly tested to catch bugs and issues.
   - It only moves forward once all defects are resolved.

6. **Deployment**  
   - The tested software is moved to the **production environment** where real users can interact with it.

7. **Maintenance**  
   - Keeping the app running smoothly.
   - Applying updates, fixing issues, and adapting to changes over time.

**Explanation:**  
This step-by-step process is structured and ensures quality. The operations team plays a critical role post-deployment, ensuring the software stays available and stable.

---

#### 🔄 Software Development Models

**1. Waterfall Model:**  
   - Each phase is done **sequentially**.
   - Once a phase is completed, you **can’t go back**.
   - Working software is seen **very late**, possibly months into development.
   - Not ideal if requirements are **uncertain or evolving**, like in Emma’s case.

**2. Agile Model:**  
   - Requirements are broken into **smaller tasks (sprints/iterations)**.
   - Iterations typically last **2 to 4 weeks**.
   - Each sprint delivers a **working prototype** or feature.
   - Stakeholders like Emma can give **frequent feedback**, helping shape the final product as it evolves.

**Explanation:**  
Agile offers **flexibility**. It’s best when clients are unsure about all features upfront, or when they may change ideas as the product takes shape.

---

#### ⚠️ Challenges with Agile SDLC – Developer vs. Operations

**Problem Emerges:**  
As development progresses using Agile, the **operations team (ops)** faces difficulties in keeping up:
- Code needs to be **frequently deployed** for testing.
- Testers sometimes **can’t access** the servers, or test cases fail.
- Deployment instructions may be **unclear** or miscommunicated.

**Explanation:**  
Agile demands **frequent updates**. The ops team is burdened by:
- Constant deployment requests.
- Managing server uptime.
- Fixing issues on short notice.

This leads to **missed deadlines**, frustration, and ultimately delays in product delivery — making Emma (the client) unhappy.

---

#### 🚧 Wall Between Dev and Ops

**The Great Divide:**  
- **Developers** throw their code "over the wall".
- **Operations** team has to figure out how to deploy it.
- Devs complain about **slow deployments**.
- Ops complains about **poor instructions and pressure**.

**Real-world Consequences:**  
- **Delays and bugs** in production.
- **Unhappy customers** and **lost business**.
- Development and operations are **misaligned**, even though they’re on the same project.

**Analogy:**  
Developers are **Agile** — quick and iterative.  
Operations are **ITIL (Waterfall)-driven** — structured and stability-focused.  
This clash causes friction.

---

#### 🚀 Introduction to DevOps

**Reggie’s Realization:**  
Reggie, the director, identifies the root cause:  
Dev and Ops aren’t **collaborating effectively**.

**Solution: DevOps**  
- A **DevOps consultant** is brought in to unify and streamline the process.
- The goal isn’t magic — it’s **collaboration, communication, and integration**.

---

#### 🔧 DevOps in Action – Breaking the Wall

**Training and Culture Shift:**  
- **Developers** are trained in operations concepts (e.g., server behavior, deployment pipelines).
- **Operations** are trained in Agile concepts (e.g., iterations, sprints).
- Every team is introduced to **automation tools and techniques**.

**Automation in DevOps:**  
All key tasks are automated:
- **Code building**
- **Testing (unit and integration)**
- **Infrastructure provisioning**
- **Software deployment**

Automation ensures:
- **No human errors**
- **Faster and repeatable** delivery process

**Explanation:**  
Instead of handing things over blindly, both teams:
- **Work together**
- Use **automated pipelines**
- Share knowledge and responsibility

---

#### 🛠️ DevOps Lifecycle – Fully Automated Flow

**Key Features:**
- **No manual intervention**
- **Quick iterations**
- Everything is **integrated and streamlined**
- Ensures **consistency**, **efficiency**, and **rapid delivery**

**Outcome:**  
- Any request Emma makes can now be fulfilled **quickly**.
- Customers are **satisfied** with timely updates and a stable experience.
- Emma's idea has **successfully scaled into a thriving online business**.

---

#### 🎉 Summary

**Before DevOps:**
- Siloed teams.
- Miscommunication.
- Delays in development and deployment.
- Frustrated stakeholders.

**After DevOps:**
- Seamless collaboration.
- Automated pipelines.
- Continuous delivery and integration.
- Happy customers and business growth.

---

### DevOps Principles, Practices, and Culture

#### 🧭 **DevOps Principles**

DevOps is not just a set of tools—**it’s a philosophy, a mindset, and a set of principles** that guide teams to deliver better software faster and more reliably.

1. **Collaboration and Communication**  
   DevOps breaks down silos between development and operations teams, fostering continuous collaboration and shared responsibilities.

2. **End-to-End Responsibility**  
   Teams own the software across its entire lifecycle, from development to maintenance.

3. **Continuous Improvement**  
   Focuses on small, frequent updates, retrospectives, and learning from failures.

4. **Automation First**  
   Automates repetitive tasks to save time and improve reliability.

5. **Customer-Centric Action**  
   Aligns technical efforts with customer satisfaction and business outcomes.

---

#### 🛠️ **DevOps Practices**

1. **Continuous Integration (CI)**  
   Frequent code merges with automated builds and tests to ensure quality.

2. **Continuous Delivery (CD)**  
   Prepares code for production with automated deployment to production-like environments.

3. **Infrastructure as Code (IaC)**  
   Manages infrastructure using code for consistency and repeatability.

4. **Automated Testing**  
   Includes unit, integration, and end-to-end tests integrated into CI/CD pipelines.

5. **Monitoring and Logging**  
   Real-time monitoring and insights for performance and reliability.

6. **Configuration Management**  
   Maintains consistency of software performance across environments.

7. **Version Control for Everything**  
   Applies version control to source code, infrastructure, configurations, and pipelines.

8. **Security as Code (DevSecOps)**  
   Integrates security practices into the development lifecycle.

---

#### 🌱 **DevOps Culture**

1. **Blameless Culture**  
   Focuses on learning from failures and improving systems rather than assigning blame.

2. **Shared Ownership**  
   Encourages empathy and shared responsibilities among all roles.

3. **Learning and Experimentation**  
   Promotes a growth mindset and experimentation as paths to innovation.

4. **Agility and Flexibility**  
   Thrives in environments where rapid changes and adaptability are critical.

5. **Feedback Loops**  
   Embeds constant feedback loops for continuous improvement.

6. **Tooling Supports Culture, Not Defines It**  
   Tools enable collaboration and efficiency but are not the foundation of DevOps.

---

### The DevOps Lifecycle

The **DevOps lifecycle** represents a continuous and collaborative approach to software development and operations. The lifecycle is **not linear**, but rather a **cyclic process** where every phase feeds into the next, enabling continuous feedback, improvement, and automation.

---

#### Plan

**Overview:**  
The **Plan** phase is the foundation of the DevOps lifecycle. It involves defining the vision, objectives, requirements, features, and tasks needed to build a software application.

**Key Activities:**
- Requirements gathering (functional and non-functional)
- Roadmap creation
- Sprint planning (Agile boards)
- Task breakdown and assignments
- Estimating effort and deadlines
- Identifying dependencies and risks

**Tools:**
- **Jira**, **Trello**, **Asana** – Task and sprint management
- **Confluence**, **Notion** – Documentation
- **Slack**, **Teams** – Communication and collaboration

**Goals:**
- Align team objectives with business goals
- Create clarity and visibility into upcoming work
- Establish a repeatable planning cadence (often through Agile sprints)

---

#### Build

**Overview:**  
This phase involves **actual software development**. The code is written and stored in a version control system, then built into executable form.

**Key Activities:**
- Writing code
- Version control and code branching
- Compiling or bundling source code
- Resolving dependencies
- Packaging the build into an **artifact**

**Tools:**
- **Git**, **GitHub**, **GitLab**, **Bitbucket** – Source code management
- **Maven**, **Gradle**, **npm**, **pip** – Build tools
- **Docker** – Containerizing the build
- **Jenkins**, **GitHub Actions** – Build orchestration

**Goals:**
- Generate stable, reproducible builds
- Enable developers to collaborate through version control
- Ensure rapid integration and iteration of code changes

---

#### Test

**Overview:**  
Testing ensures the quality, security, and performance of the application before it progresses further in the pipeline.

**Key Activities:**
- **Unit testing** – Checks individual components
- **Integration testing** – Verifies combined components
- **UI testing** – Ensures visual and functional correctness
- **Regression testing** – Confirms old features still work
- **Security and performance testing**

**Tools:**
- **JUnit**, **PyTest**, **TestNG** – Unit testing
- **Selenium**, **Cypress** – UI testing
- **Postman**, **SoapUI** – API testing
- **JMeter**, **LoadRunner** – Load and performance testing
- **OWASP ZAP**, **SonarQube** – Security testing

**Goals:**
- Detect bugs and vulnerabilities early
- Automate repeatable tests to ensure consistency
- Deliver high-quality, stable software

---

#### Release

**Overview:**  
The release phase is the **approval and readiness step** before deployment. The software is reviewed and scheduled for release into production or staging environments.

**Key Activities:**
- Final review and approval
- Creating a release candidate
- Versioning and tagging the release
- Notifying stakeholders (QA, product, ops)
- Change management and release documentation

**Tools:**
- **Jenkins**, **Travis CI**, **GitLab CI/CD**
- **Octopus Deploy**
- **ServiceNow**, **Jira Service Desk** – Change approvals

**Goals:**
- Ensure release is aligned with business needs
- Coordinate across teams (Dev, QA, Ops)
- Reduce risks through staged and controlled releases

---

#### Deploy

**Overview:**  
Deployment moves the tested release into the **target environments** (e.g., production, staging). This process should be **automated**, **reliable**, and **repeatable**.

**Key Activities:**
- Infrastructure provisioning
- Configuration management
- Artifact deployment
- Rolling updates / Blue-Green / Canary deployments
- Downtime management or zero-downtime deployment

**Tools:**
- **Ansible**, **Chef**, **Puppet** – Server automation
- **Terraform**, **Pulumi** – Infrastructure as code
- **Docker**, **Kubernetes** – Container orchestration
- **Spinnaker**, **ArgoCD** – Kubernetes-native deployment

**Goals:**
- Reduce lead time to deploy
- Ensure fast, reliable deployment pipelines
- Enable rollback in case of failure

---

#### Monitor

**Overview:**  
Once software is deployed, the next step is to **monitor its performance, availability, errors, and usage**. This provides immediate feedback about production issues.

**Key Activities:**
- Uptime monitoring
- Logging and alerting
- User behavior and crash analysis
- Resource consumption (CPU, memory, etc.)
- Business metrics tracking

**Tools:**
- **Prometheus**, **Grafana** – Infrastructure and app metrics
- **Datadog**, **New Relic**, **Dynatrace** – APM tools
- **ELK Stack (Elasticsearch, Logstash, Kibana)** – Log aggregation
- **Sentry**, **Rollbar** – Error tracking

**Goals:**
- Detect failures and performance issues early
- Enable proactive issue resolution
- Understand system behavior and user experience

---

#### Operate

**Overview:**  
This phase involves maintaining and managing the application and infrastructure in a **production environment**.

**Key Activities:**
- Responding to incidents and outages
- Scaling infrastructure based on demand
- Routine maintenance (patches, updates)
- Optimizing performance and cost

**Tools:**
- **PagerDuty**, **Opsgenie** – Incident response
- **AWS CloudWatch**, **Azure Monitor**, **Google Stackdriver**
- **Kubernetes**, **Nomad** – Orchestration and self-healing
- **Terraform**, **Ansible** – Maintenance automation

**Goals:**
- Ensure 24x7 application availability
- Maintain compliance, reliability, and performance
- Minimize manual intervention using automation and auto-scaling

---

#### The DevOps Lifecycle Loop

The DevOps lifecycle is iterative and continuous:
 
- Feedback from **Monitor** and **Operate** feeds into **Plan** again.
- The process becomes **faster and more efficient over time** due to automation, testing, and CI/CD pipelines.
- **Culture, automation, measurement, and sharing (CAMS)** are central principles.

---

### Docker – Detailed Notes

#### Why was Docker Needed?

**Personal Experience Introduction:**

The speaker shares a real-world project scenario where they needed to build a complete application stack. It included various technologies like:

- NodeJS for the web server
- MongoDB as the database
- Redis for messaging
- An orchestration tool for coordination

**Challenges faced:**

- **OS Compatibility Issues:**
    
    Every component (NodeJS, MongoDB, Redis, etc.) needed to be compatible with the operating system being used. Sometimes a version mismatch forced the team to look for another OS altogether.
    
- **Library and Dependency Conflicts:**
    
    Different services required different versions of the same libraries. This created conflicts and required constant management.
    
- **Changing Application Architecture:**
    
    As the application evolved — upgrading databases or components — the team had to repeatedly verify compatibility each time a change was made.
    
- **Developer Onboarding Difficulties:**
    
    Setting up a development environment for a new developer was tedious. They had to follow a long list of steps and manually configure everything correctly, including using the exact OS and component versions.
    
- **Environment Inconsistency:**
    
    Developers, testers, and production environments could differ (e.g., different operating systems), leading to problems where an app that worked in one environment failed in another.

**Conclusion:**

Managing the application lifecycle (development, building, shipping) became extremely painful.

Thus, a solution was needed that:

- Handled compatibility better
- Allowed isolated setups of services
- Provided easy setup for developers

**Discovery:**

This problem led the speaker to discover **Docker**.

---

#### How Docker Helped

- **Containers for Each Component:**
    
    Each application component was run inside its own **container**. Each container had its **own dependencies and libraries**.
    
- **One-Time Configuration:**
    
    The Docker setup was built once. Afterwards, developers only had to run a simple `docker run` command to spin up the required environment.
    
- **OS Independence:**
    
    As long as Docker was installed, it didn't matter what OS the developer was using. The container would work the same way everywhere.

---

#### What are Containers?

- **Isolated Environments:**
    
    A container is a completely isolated environment that has:
    
    - Its own processes and services
    - Its own network interfaces
    - Its own mounts
- **Difference from Virtual Machines:**
    
    Although they behave somewhat like VMs, **containers share the same OS kernel** of the host system, unlike VMs which require their own OS.
    
- **History:**
    
    Containers are not new — technologies like **LXC, LXD, LXCFS** have existed for over a decade.
    
    Docker popularized containers by building a **high-level, user-friendly platform** on top of these low-level technologies.

---

#### Revisiting Operating System Concepts

- **Structure of an OS:**
    
    Any Linux-based OS (Ubuntu, Fedora, CentOS, etc.) consists of:
    
    - **Kernel:** Manages hardware interactions.
    - **Software Stack:** Things like user interfaces, drivers, compilers, developer tools, etc.
- **Kernel Sharing in Containers:**
    
    Docker containers **share the host machine's kernel** but have their **own software stack** on top.
    
    Example:
    
    - An Ubuntu-based Docker host can run Debian, Fedora, or CentOS containers easily — all of them use the Linux kernel.
- **Windows and Docker:**
    - **Problem:** Windows has a different kernel than Linux, so you **cannot natively** run Linux containers on Windows.
    - **Solution:** When Docker is installed on Windows, it **spins up a lightweight Linux Virtual Machine** internally to run Linux containers.
    
    Hence, Linux containers on Windows are actually Linux containers running inside a hidden Linux VM.

---

#### Containers vs Virtual Machines (VMs)

| Aspect | Containers | Virtual Machines |
| --- | --- | --- |
| OS | Share host OS kernel | Each VM has its own OS |
| Resource Usage | Lightweight (Megabytes) | Heavy (Gigabytes) |
| Boot Time | Seconds | Minutes |
| Isolation | Less strict (shared kernel) | Strong isolation |
| Flexibility | Run apps built for same kernel | Run apps built for different kernels (Linux/Windows) |

**Key Insight:**

Docker containers are **not a replacement** for VMs — they complement each other.

In real-world deployments:

- Virtual machines are still used to host Docker containers.
- One VM may now host **hundreds or thousands** of lightweight containers instead of just one application.

---

#### How Applications are Deployed with Docker

- **Public Docker Hub:**
    
    Many common applications (OS images, databases, developer tools) are already containerized and available on Docker Hub (official repository).
    
- **Simple Deployment:**
    
    After installing Docker on a host, deploying applications becomes as simple as:
    
    ```bash
    docker run <image-name>
    ```
    
    Examples:
    
    - Run an instance of MongoDB
    - Run Redis
    - Run a NodeJS server
- **Scaling:**
    
    If more instances of a service are needed:
    
    - Simply spin up more containers.
    - Use a **load balancer** in front to distribute traffic.
- **Failure Handling:**
    
    If a container fails:
    
    - Destroy the bad container.
    - Launch a new one easily and quickly.

---

#### Images vs Containers

- **Image:**
    - A static template or package that contains the code, libraries, and dependencies.
    - Think of it like a VM template.
- **Container:**
    - A **running instance** of an image.
    - It's live, isolated, and has its own environment and processes.

**Creating Custom Images:**

If an organization needs something custom not found on Docker Hub:

- They can **build their own image**.
- Push it to Docker Hub (private or public).

---

#### Docker's Role in DevOps

- **Traditional Approach:**
    
    Developers built the application → Gave it to Operations → Ops struggled to set it up manually.
    
- **With Docker:**
    - Developers and Ops teams **collaborate** on a **Dockerfile**.
    - This Dockerfile includes all setup instructions and requirements.
    - A Docker Image is built from the Dockerfile.
    - The same image is used in development, testing, and production.

**Benefits:**

- Eliminates the "it worked on my machine" problem.
- Ensures consistency across environments.
- Speeds up deployment.

---

#### Docker Installation Guide

##### Step 1: Install Oracle VirtualBox

- Download and install **Oracle VirtualBox** from the official website.
- Install it on your **Windows laptop**.

##### Step 2: Create an Ubuntu VM

- Download an **Ubuntu ISO** (LTS version recommended, e.g., Ubuntu 22.04).
- Open VirtualBox and create a **new VM**:
    - Select "Linux" as the type and "Ubuntu" as the version.
    - Allocate memory (RAM) and disk space.
- Attach the Ubuntu ISO in the VM settings → **Storage** → **Add ISO**.
- Boot the VM and install Ubuntu by following the on-screen instructions.

##### Step 3: Install Docker on Ubuntu

Open the **terminal** inside the Ubuntu VM and follow these steps:

1. **Update package index:**
    
    ```bash
    sudo apt update
    ```
    
2. **Install required packages:**
    
    ```bash
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    ```
    
3. **Add Docker's official GPG key:**
    
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```
    
4. **Set up the Docker repository:**
    
    ```bash
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```
    
5. **Update package index again (after adding Docker repo):**
    
    ```bash
    sudo apt update
    ```
    
6. **Install Docker Engine:**
    
    ```bash
    sudo apt install docker-ce
    ```

---

##### Step 4: Start Docker Service

- Start the Docker service:
    
    ```bash
    sudo service docker start
    ```
    
- (Optional) To enable Docker to start automatically on boot:
    
    ```bash
    sudo systemctl enable docker
    ```

---

##### Step 5: Test Docker Installation

- Run the **hello-world** container:
    
    ```bash
    sudo docker run hello-world
    ```
    
    - ✅ Docker ran successfully with `sudo`.
- Try running without `sudo`:
    
    ```bash
    docker run hello-world
    ```
    
    - ❌ **Error**: Permission denied (expected).

---

##### Step 6: Run Docker Without `sudo`

- Add your user to the `docker` group:
    
    ```bash
    sudo usermod -aG docker $USER
    ```
    
- **Important:** After running the above command, **log out and log back in** (or restart the VM) so that group changes take effect.
- Now try running again:
    
    ```bash
    docker run hello-world
    ```
    
    - ✅ **Success!** Docker now works without `sudo`.

---

#### Basic Docker Commands

##### 1. Running a Docker Container

- Command:
    
    ```bash
    docker run <image-name>
    ```
    
- **Example**:
    
    ```bash
    docker run centos
    ```
    
- Behavior:
    - Docker checks if the image exists locally.
    - If not, Docker downloads (pulls) it from **Docker Hub**.
    - Official images (e.g., centos, ubuntu, nginx) can be pulled just by name.

---

##### 2. Running a Container with a Command

- To keep a container running (otherwise it exits immediately):
    - Provide a command like `bash` or `sleep`.
    - Example to open bash inside a CentOS container:
        
        ```bash
        docker run -it centos bash
        ```
        
    - `it` options:
        - `i`: Interactive mode (keeps STDIN open)
        - `t`: Allocates a pseudo-TTY (terminal)

---

##### 3. Listing Containers

- **List running containers**:
    
    ```bash
    docker ps
    ```
    
- **List all containers (running + exited)**:
    
    ```bash
    docker ps -a
    ```

---

##### 4. Running Containers in Detached Mode

- Run containers in background (detached):
    
    ```bash
    docker run -d centos sleep 20
    ```
    
- `d`: Detached mode (container runs in background)
- Can still check them using `docker ps`.

---

##### 5. Stopping and Killing Containers

- **Stop a running container**:
    
    ```bash
    docker stop <container-name-or-ID>
    ```
    
- After stopping, container is listed as **Exited** in `docker ps -a`.
- Exit codes:
    - `0` → Normal exit
    - `137` → Force-stopped or killed

---

##### 6. Removing Containers

- **Remove one container**:
    
    ```bash
    docker rm <container-name-or-ID>
    ```
    
- **Remove multiple containers**:
    
    ```bash
    docker rm <container-ID-1> <container-ID-2> <container-ID-3>
    ```
    
- Tip: You don't have to type the full ID, just the first few characters.

---

##### 7. Viewing Docker Images

- **List downloaded images**:
    
    ```bash
    docker images
    ```
    
- Displays:
    - Repository
    - Tag
    - Image ID
    - Size

---

##### 8. Removing Docker Images

- **Remove an image**:
    
    ```bash
    docker rmi <image-name>
    ```
    
- **Note**:
    
    You cannot delete an image if containers are still using it.
    
    - First, remove the containers:
        
        ```bash
        docker rm <container-ID>
        ```
        
    - Then remove the image.

---

##### 9. Pulling an Image without Running It

- **Pull image only** (without running):
    
    ```bash
    docker pull <image-name>
    ```

---

##### 10. Quick Notes on Image Repositories

- **Official images**:
    - Pulled directly by name (e.g., `centos`, `ubuntu`).
- **Personal or custom images**:
    - Use format:
        
        ```
        <dockerhub-username>/<repository-name>
        ```
        
    - Example:
        
        ```bash
        docker run mmsumshad/ansible-playable
        ```

---

### Summary of Common Commands

| Action | Command Example |
| --- | --- |
| Run a container | `docker run centos` |
| Run interactively | `docker run -it centos bash` |
| List running containers | `docker ps` |
| List all containers | `docker ps -a` |
| Stop a container | `docker stop <container-ID>` |
| Remove a container | `docker rm <container-ID>` |
| List images | `docker images` |
| Remove an image | `docker rmi <image-name>` |
| Pull an image manually | `docker pull <image-name>` |

---

#### Docker Run in Detail

##### 1. Running Specific Versions of Images (Tags)

- **Concept:**
    
    Docker images have different versions identified by **tags**.
    
- **Default Behavior:**
    - If you don't specify a tag, Docker pulls the image tagged as **`latest`**.
- **Command to run specific version:**
    
    ```bash
    docker run redis:4.0
    ```
    
- **Explanation:**
    - `redis` = Image name
    - `4.0` = Specific version tag
    - `:` separates image name and version.
- **Where to find available tags:**
    - Visit **Docker Hub**.
    - Check under the image description for available tags.

---

##### 2. Running Containers in Interactive Mode

- **Problem:**
    
    By default, Docker containers **do not accept standard input** (non-interactive).
    
- **Solution: Use `i` for interactive mode**
    
    ```bash
    docker run -i <image-name>
    ```
    
- **Explanation:**
    - `i` keeps the standard input (stdin) open for the container even if not attached.

---

##### 3. Attaching a Terminal (Pseudo-TTY)

- **Problem:**
    
    Prompts (like "Enter your name:") **don't appear** without terminal attachment.
    
- **Solution: Use `t` to allocate a pseudo-TTY**
    
    ```bash
    docker run -t <image-name>
    ```
    
- **Interactive + Terminal together:**
    
    ```bash
    docker run -it <image-name>
    ```
    
- **Explanation:**
    - `i` for interactive input
    - `t` for pseudo-terminal
    - `it` combines both for full interaction with the container.

---

##### 4. Port Mapping / Publishing Ports

- **Problem:**
    
    Container ports are **not directly accessible** from outside the Docker host.
    
- **Solution: Use `p` to map ports**
- **Command:**
    
    ```bash
    docker run -p <host-port>:<container-port> <image-name>
    ```
    
- **Example:**
    
    ```bash
    docker run -p 80:5000 my-web-app
    ```
    
- **Explanation:**
    - Maps port `5000` inside the container to port `80` on the Docker host.
    - Access app via `http://<Docker-host-IP>:80`.
- **Important Notes:**
    - **Container IP** (e.g., 172.17.0.2) is internal, only accessible inside Docker host.
    - **Docker Host IP** (e.g., 192.168.1.5) is external and can be used if port mapped.
    - **Cannot map the same host port** to multiple containers.
- **Multiple Applications Example:**
    - MySQL instance 1 → Host port 3306 → Container port 3306
    - MySQL instance 2 → Host port 8306 → Container port 3306

---

##### 5. Data Persistence Using Volumes

- **Problem:**
    
    If a container is deleted, **data inside it is lost**.
    
- **Solution: Use `v` to mount host directories**
- **Command:**
    
    ```bash
    docker run -v <host-dir>:<container-dir> <image-name>
    ```
    
- **Example:**
    
    ```bash
    docker run -v /opt/data:/var/lib/mysql mysql
    ```
    
- **Explanation:**
    - Maps `/opt/data` on the host to `/var/lib/mysql` inside container.
    - Data stored in `/opt/data` **persists** even if the container is deleted.

---

##### 6. Viewing Detailed Container Information

- **Command:**
    
    ```bash
    docker inspect <container-id or container-name>
    ```
    
- **Explanation:**
    - Displays detailed JSON output including:
        - State
        - Mounts
        - Network settings
        - Configuration details

---

##### 7. Viewing Container Logs

- **Command:**
    
    ```bash
    docker logs <container-id or container-name>
    ```
    
- **Explanation:**
    - Shows all standard output logs from a container.
    - Useful for containers running in **detached mode** (`d`).

---

### 🔥 Quick Command Summary

| Action | Command Example | Description |
| --- | --- | --- |
| Run container with tag | `docker run redis:4.0` | Run specific version of image |
| Interactive mode | `docker run -i ubuntu` | Keep STDIN open |
| Pseudo-terminal | `docker run -t ubuntu` | Allocate TTY |
| Interactive + TTY | `docker run -it ubuntu` | Full interactive terminal session |
| Port mapping | `docker run -p 80:5000 webapp` | Map host port to container port |
| Mount volume | `docker run -v /opt/data:/var/lib/mysql mysql` | Persist container data outside |
| Inspect container | `docker inspect container-id` | View detailed container info |
| View logs | `docker logs container-id` | View container logs |

---

## Dockerizing a Simple Python Flask Application

### Application Overview

This section demonstrates how to containerize a basic Python Flask web application using Docker. The application exposes two endpoints:

- `/` returns a "Welcome" message.
- `/how-are-you` returns "I'm good, how about you?"

You can find the implementation in:
- [my-simple-webapp-flask/app.py](my-simple-webapp-flask/app.py)
- [my-simple-webapp-flask/Dockerfile](my-simple-webapp-flask/Dockerfile)

---

### Manual Deployment Steps

To manually deploy the application on an Ubuntu host:

1. **Install Python**:
    ```bash
    apt-get update
    apt-get install -y python3
    ```

2. **Install pip**:
    ```bash
    apt-get install -y python3-pip
    ```

3. **Install Flask**:
    ```bash
    pip3 install flask
    ```

4. **Deploy the Application**:
    ```bash
    cp /path/to/app.py /opt/app.py
    flask --app /opt/app.py run --host=0.0.0.0
    ```

Once running, access the app at `http://<host-ip>:5000`.

---

### Dockerizing the Application

1. **Create a Dockerfile**:  
   The Dockerfile defines the steps to containerize the application:
   - Use the official Ubuntu image.
   - Install Python, pip, and Flask.
   - Copy `app.py` into the container.
   - Set the entrypoint to run the Flask app.

2. **Dockerfile Example** ([my-simple-webapp-flask/Dockerfile](my-simple-webapp-flask/Dockerfile)):
    ```docker
    FROM ubuntu

    RUN apt-get update && apt-get install -y python3 python3-pip python3-flask

    COPY app.py /opt/app.py

    ENTRYPOINT ["flask", "--app", "/opt/app.py", "run", "--host=0.0.0.0"]
    ```

#### Explanation:

- `FROM ubuntu`: Uses Ubuntu as the base image.
- `RUN ...`: Installs Python 3, pip, and Flask.
- `COPY app.py /opt/app.py`: Copies the application code.
- `ENTRYPOINT ...`: Runs the Flask app on container start.

---

### Build and Run the Docker Image

1. **Build the Docker Image** (run in the [my-simple-webapp-flask](my-simple-webapp-flask/) directory):
    ```bash
    docker build -t my-simple-webapp .
    ```

2. **Run the Docker Container**:
    ```bash
    docker run -d -p 5000:5000 my-simple-webapp
    ```

3. **Access the Application**:
    - [http://localhost:5000](http://localhost:5000) for the root endpoint.
    - [http://localhost:5000/how-are-you](http://localhost:5000/how-are-you) for the second endpoint.

---

### Pushing the Docker Image to Docker Hub

1. **Tag the Image**:
    ```bash
    docker tag my-simple-webapp yourdockerhubusername/my-simple-webapp
    ```

2. **Login to Docker Hub**:
    ```bash
    docker login
    ```

3. **Push the Image**:
    ```bash
    docker push yourdockerhubusername/my-simple-webapp
    ```

4. **Pull the Image** (on any machine):
    ```bash
    docker pull yourdockerhubusername/my-simple-webapp
    ```

---

### Conclusion

This section covered:

1. Creating a simple Python Flask application ([my-simple-webapp-flask/app.py](my-simple-webapp-flask/app.py)).
2. Writing a Dockerfile to containerize it ([my-simple-webapp-flask/Dockerfile](my-simple-webapp-flask/Dockerfile)).
3. Building and running the Docker image.
4. Pushing the image to Docker Hub for sharing and reuse.

Containerizing applications with Docker ensures consistent deployments across different environments.

---

## Environment Variables in Docker

- **Problem**:  
  Hardcoding configuration (like background color) in application code is bad practice.

- **Solution**:  
  Move dynamic values (like `APP_COLOR`) to **environment variables**.

- **How to set environment variables**:
    - During normal execution:
        ```bash
        export APP_COLOR=blue
        ```
    - During Docker container run:
        ```bash
        docker run -e APP_COLOR=blue image-name
        ```

- **Deploy multiple containers with different configurations**:  
  Set different `-e` values each time.

- **View environment variables of a running container**:
    ```bash
    docker inspect container-name
    ```
    Look under the **Config > Env** section.

---

## Commands, Arguments, and Entrypoints in Docker

### Understanding Container Lifecycle

- **Container behavior**:  
  A container **runs a process**. If the process ends, the container **stops**.

- **Example**:  
  Running `docker run ubuntu` without a command → container exits immediately (default bash process tries to find a terminal, fails, and exits).

### CMD Instruction

- **CMD in Dockerfile**:  
  Specifies the default command for the container when it starts.

- **Example**:  
  Ubuntu image has CMD as `["bash"]`.

- **Override CMD during run**:
    ```bash
    docker run ubuntu sleep 5
    ```
    - Runs `sleep 5` instead of default `bash`.

- **Ways to write CMD**:
    - **Shell form**:
        ```
        CMD sleep 5
        ```
    - **Exec form (preferred)**:
        ```
        CMD ["sleep", "5"]
        ```

### ENTRYPOINT Instruction

- **ENTRYPOINT**:  
  Defines a **fixed executable** that **always runs** when the container starts.

- **Behavior**:
    - Command-line arguments during `docker run` are **appended** to ENTRYPOINT.
    - Unlike CMD, ENTRYPOINT is **not replaced** by command-line arguments.

- **Example** ([cmd-vs-entrypoint/Dockerfile](cmd-vs-entrypoint/Dockerfile)):
    ```
    ENTRYPOINT ["sleep"]
    CMD ["5"]
    ```
    - Default command: `sleep 5`
    - If you run:
        ```bash
        docker run ubuntu-sleeper 10
        ```
        It runs: `sleep 10`

- **CMD provides default parameters** when none are passed at runtime.

### Overriding ENTRYPOINT at runtime

- **Use `--entrypoint` option**:
    ```bash
    docker run --entrypoint sleep2.0 ubuntu-sleeper 10
    ```
    - Changes executable from `sleep` to `sleep2.0`.

---

## Important Dockerfile Summary

| Dockerfile Instruction | Purpose | Behavior |
| --- | --- | --- |
| `CMD` | Default command | Replaced if user provides one in `docker run` |
| `ENTRYPOINT` | Fixed executable | Arguments appended; executable stays the same |
| `CMD` + `ENTRYPOINT` | Together | ENTRYPOINT + CMD args at startup |

---

---

## Docker Compose

### 🔧 Docker Basics Recap

- Use `docker run` to start individual containers.
- For complex multi-service applications, use **Docker Compose** with a YAML configuration.

---

### 🐳 Sample Voting Application Stack (Used Throughout the Course)

#### Components

1. **Voting App (Python)**
    - Lets users vote between *cats* and *dogs*.
    - Votes stored temporarily in **Redis**.
2. **Worker (.NET)**
    - Fetches votes from Redis.
    - Updates final tally in **PostgreSQL**.
3. **Result App (Node.js)**
    - Reads tally from PostgreSQL.
    - Displays results via web UI.

#### Data Flow

User ➝ Voting App ➝ Redis ➝ Worker ➝ PostgreSQL ➝ Result App

---

### 🐳 Running Each Service via `docker run`

- **Redis:**
    ```bash
    docker run -d --name redis redis
    ```
- **PostgreSQL:**
    ```bash
    docker run -d --name db postgres
    ```
- **Voting App:**
    ```bash
    docker run -d --name vote -p 5000:80 vote-app
    ```
- **Result App:**
    ```bash
    docker run -d --name result -p 5001:80 result-app
    ```
- **Worker:**
    ```bash
    docker run -d --name worker worker-app
    ```

---

### 🔗 Container Communication Using `--link` (Deprecated)

- Use `--link` to allow inter-container communication by hostname.
    ```bash
    docker run --link redis:redis ...
    ```
    - Updates `/etc/hosts` with `redis` name pointing to container IP.
- **Worker needs links to both Redis and PostgreSQL.**

> **Note:** `--link` is deprecated. Docker Compose (v2+) with networking is preferred.

---

### 🛠️ Docker Compose File (Basic Structure)

See: [example-voting-app-main/docker-compose.yml](example-voting-app-main/docker-compose.yml)

---

### 🏗️ Key Docker Compose Concepts

- `services:` – All containers go under this section (from v2 onwards).
- `build:` – Specifies directory with Dockerfile to build image.
- `image:` – For prebuilt/public images (like `redis`, `postgres`).
- `ports:` – Host:Container port mappings.
- `depends_on:` – Define startup order (e.g., vote depends on redis).

---

### 📁 Build vs Pull

- Use `image:` if pulling from Docker Hub.
- Use `build:` if building from local directory with a Dockerfile.

---

### 🌐 Networking Differences

- **v1:** All containers attached to the default bridge network. Use `links`.
- **v2+:** Docker Compose creates a new bridge network automatically. Services can talk to each other using service names (no need for `links`).

---

### 🧾 Docker Compose Versions Summary

| Feature | Version 1 | Version 2+ |
| --- | --- | --- |
| File structure | Flat service definitions | Nested under `services:` |
| Networking | Default bridge + `links` | Automatic app-specific network |
| Startup order | ❌ Not supported | ✅ `depends_on:` available |
| Version declaration | ❌ Not required | ✅ `version: '2'` required |

---

## 🧱 Voting App Architecture

The Example Voting App is a **multi-tier application** with 5 main components:

| Component | Language / Tech | Purpose |
| --- | --- | --- |
| `vote` | Python + Flask | Frontend web app to cast votes (cats/dogs) |
| `redis` | Redis | Queue to temporarily store votes |
| `worker` | .NET | Pulls vote from Redis → saves to Postgres |
| `db` (postgres) | PostgreSQL | Stores votes persistently |
| `result` | Node.js + Express | Displays voting results |

---

## 📂 Repository Structure

- [`example-voting-app-main/vote/`](example-voting-app-main/vote/) → Flask app (Python)
- [`example-voting-app-main/worker/`](example-voting-app-main/worker/) → Worker app (.NET)
- [`example-voting-app-main/result/`](example-voting-app-main/result/) → Result app (Node.js)
- [`example-voting-app-main/docker-compose.yml`](example-voting-app-main/docker-compose.yml), `stack.yml`

---

## 🔄 Flow of Data

1. User votes on `vote` app
2. Vote is pushed to **Redis**
3. `worker` fetches vote from Redis, inserts into **Postgres**
4. `result` app queries Postgres and displays the current tally

---

## 🔧 Step-by-Step Deployment (Manual Docker)

### 1️⃣ Clone Repo

```bash
git clone https://github.com/dockersamples/example-voting-app.git
cd example-voting-app
```

---

### 2️⃣ Deploy `redis` (Detached)

```bash
docker run -d --name redis redis
```

---

### 3️⃣ Build & Run `vote` App

```bash
cd vote
docker build -t voting-app .
docker run -d --name vote --link redis -p 5000:80 voting-app
```

- Web UI accessible at: `http://localhost:5000`
- Votes won't work yet → Redis exists, but worker & DB are missing

---

### 4️⃣ Deploy `postgres` (Named `db`, Detached)

```bash
docker run -d --name db -e POSTGRES_PASSWORD=example postgres:9.4
```

---

### 5️⃣ Build & Run `worker` App

```bash
cd ../worker
docker build -t worker-app .
docker run -d --name worker --link redis --link db worker-app
```

---

### 6️⃣ Build & Run `result` App

```bash
cd ../result
docker build -t result-app .
docker run -d --name result --link db -p 5001:80 result-app
```

- Result UI at: `http://localhost:5001`

---

## 🐳 Containers Summary (`docker ps`)

| Container | Port | Links | Purpose |
| --- | --- | --- | --- |
| vote | 5000:80 | redis | Frontend |
| redis | - | - | Queue |
| worker | - | redis, db | Redis → Postgres bridge |
| db | - | - | Database |
| result | 5001:80 | db | Result visualizer |

---

## 🧪 Troubleshooting Tips

- `500 Internal Server Error` → Happens if `redis` isn't running or linked properly.
- `Container name already in use` → Use `docker rm <name>` before recreating.
- Logs helpful: `docker logs <container>`.

---

## 📖 Continuation: Running Voting App with Docker Compose

Now that we have individual services for the voting app, result app, worker, Redis, and Postgres, let's simplify everything using **Docker Compose**.

Instead of running each container manually, we'll describe everything in a single file called [`docker-compose.yml`](example-voting-app-main/docker-compose.yml). Docker Compose will take care of building images, creating containers, connecting them via networks, and managing their dependencies.

---

## 🛠 [`docker-compose.yml`](example-voting-app-main/docker-compose.yml) file

```yaml
services:
  vote:
    build:
      context: ./vote
      target: dev
    depends_on:
      - redis
    volumes:
      - ./vote:/usr/local/app
    ports:
      - "8080:80"
    networks:
      - front-tier
      - back-tier

  result:
    build: ./result
    entrypoint: nodemon --inspect=0.0.0.0 server.js
    depends_on:
      - db
    volumes:
      - ./result:/usr/local/app
    ports:
      - "8081:80"
      - "127.0.0.1:9229:9229"
    networks:
      - front-tier
      - back-tier

  worker:
    build:
      context: ./worker
    depends_on:
      - redis
      - db
    networks:
      - back-tier

  redis:
    image: redis:alpine
    networks:
      - back-tier

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
    volumes:
      - "db-data:/var/lib/postgresql/data"
    networks:
      - back-tier

  seed:
    build: ./seed-data
    profiles: ["seed"]
    depends_on:
      - vote
    networks:
      - front-tier
    restart: "no"

volumes:
  db-data:

networks:
  front-tier:
  back-tier:
```

---

## 🧠 Explanation of what's happening

| Service | Purpose | Details |
| --- | --- | --- |
| `vote` | Front-end Voting App (Python Flask) | Listens on port 8080, connects to Redis to store votes. Code mounted for live changes. |
| `result` | Results App (Node.js) | Listens on port 8081, connects to Postgres DB to read results. Uses `nodemon` for live reloading during development. |
| `worker` | Background Processor | Fetches votes from Redis and updates Postgres with the counted votes. |
| `redis` | In-memory Data Store | Temporary store for incoming votes. Very fast. |
| `db` | Database (Postgres) | Permanent store for final vote counts. |
| `seed` | (Optional) Seed Data Generator | Populates the app with some initial data, runs once if you specify the `seed` profile manually. |

Two separate **networks** are used:

- `front-tier`: For communication between front-end apps and Redis.
- `back-tier`: For communication between worker, Redis, and database.

The `db-data` **volume** ensures that Postgres data persists even if the container is restarted.

---

## ▶️ How to run

Simply run:

```bash
docker compose up
```

You should start seeing all services starting up in the logs.

---

## 🌐 Access the Voting Application

- Open your browser and go to: [http://localhost:8080](http://localhost:8080/)
    - Here, you can **cast your vote** (for example, "Cats" vs "Dogs").
- Then open another tab: [http://localhost:8081](http://localhost:8081/)
    - Here, you can **see the real-time voting results** updating.

---

## 📋 Summary of this step

- Used `docker-compose.yml` to define everything needed.
- One command (`docker compose up`) to build and start everything.
- Voting UI available at **localhost:8080**.
- Results available at **localhost:8081**.
- Live code reloading if you change Python or Node.js code (because of volumes + dev settings).

---