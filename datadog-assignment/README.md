# Datadog Integration with Flask App on AWS EC2

## Overview

This is my completed assignment demonstrating how I set up a Flask web application on an AWS EC2 instance and integrated it with Datadog for log monitoring and observability. I'm presenting this project to showcase my work on infrastructure setup, application deployment, and monitoring configuration using industry-standard tools and practices.

## What I Accomplished

In this assignment, I successfully:
- Deployed a Flask web application on AWS EC2 from scratch
- Configured proper security groups for web traffic access
- Set up and configured Datadog monitoring agent
- Enabled comprehensive log collection and monitoring
- Troubleshot and resolved permission issues with log file access
- Created a complete end-to-end monitoring solution

## My Implementation Journey

### 1. AWS EC2 Setup

#### Accessing EC2 Console
I started by navigating to the AWS Console and searching for EC2 to access the EC2 dashboard.

![EC2 Home Page](images/EC2_home_page.png)

#### Launching EC2 Instance
I configured and launched a new EC2 instance with the following specifications:
- Instance type: t2.micro (free tier eligible)
- Operating System: Ubuntu Server
- Security group: Default (to be modified later)

![EC2 Instance Launch Configuration](images/EC2_instance_launching.png)

#### Instance Launch Success
After configuring all settings, the instance launches successfully.

![EC2 Launch Success](images/EC2_launch_success.png)

#### Verifying Running Instance
I verified that my instance was running successfully in the EC2 instances dashboard.

![EC2 Instance Running](images/EC2_instance_running.png)

### 2. Security Group Configuration

#### Modifying Inbound Rules
To allow HTTP traffic to my Flask application, I modified the security group inbound rules to allow traffic on port 80.

![Security Group Rules Modification](images/EC2_security_group_inbound_rules_changing.png)

#### Updated Security Group Rules
The security group now allows HTTP traffic on port 80 from anywhere (0.0.0.0/0).

![Security Group Rules Updated](images/EC2_security_group_inbound_rules_changed.png)

### 3. Connecting to EC2 Instance

#### SSH Connection
I connected to the EC2 instance using SSH with the provided PEM key file.

![SSH Connection to EC2](images/EC2_connect_via_SSH.png)

### 4. Flask Application Setup

#### Installing Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-flask
```

#### Creating the Flask Application
```bash
mkdir flask_app && cd flask_app
nano app.py
```

#### Flask Application Code
The `app.py` file contains a simple Flask application with two endpoints:

```python
from flask import Flask, request
import logging

app = Flask(__name__)

# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/')
def hello():
    logging.info('Home page accessed')
    return "Hello from Flask!"

@app.route('/ping')
def ping():
    logging.info('Ping endpoint hit from %s', request.remote_addr)
    return "Pong!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

**Application Features:**
- **Root endpoint (/)**: Returns a simple "Hello from Flask!" message
- **Ping endpoint (/ping)**: Returns "Pong!" and logs the client's IP address
- **Logging**: Each visit to both endpoints is logged with timestamps to `app.log` file
- **Network binding**: Runs on all interfaces (0.0.0.0) on port 80

#### Running the Application
```bash
sudo python3 app.py
```

#### Testing the Application
Access the application using the EC2 instance's public IP address:
- Home page: `http://<your-ec2-public-ip>/`
- Ping endpoint: `http://<your-ec2-public-ip>/ping`

![Flask App Home Page](images/Flask_app_homepage.png)

![Flask App Ping Page](images/Flask_app_ping_page.png)

### 5. Datadog Setup and Integration

#### Accessing Datadog
I navigated to the Datadog website to set up monitoring for my application.

![Datadog First Page](images/datadog_first_page.png)

#### Creating Account and Quickstart
After creating a free trial account, the quickstart page provides setup instructions.

![Datadog Quickstart Page](images/datadog_quickstart_page.png)

#### Agent Installation Instructions
Navigate to Integrations > Install Agent and select Linux in the Hosts section.

![Datadog Linux Integration Install Page](images/datadog_linux_integrations_install_page.png)

#### Installing Datadog Agent
I ran the following command on my EC2 instance to install the Datadog agent:

```bash
DD_API_KEY=<API_KEY> \
DD_SITE="ap1.datadoghq.com" \
DD_APM_INSTRUMENTATION_ENABLED=host \
DD_APM_INSTRUMENTATION_LIBRARIES=java:1,python:3,js:5,php:1,dotnet:3 \
bash -c "$(curl -L https://install.datadoghq.com/scripts/install_script_agent7.sh)"
```

### 6. Log Collection Configuration

#### Enable Log Collection in Agent
I edited the main Datadog agent configuration:
```bash
sudo nano /etc/datadog-agent/datadog.yaml
```

Add the following line:
```yaml
logs_enabled: true
```

#### Configure Custom Log Source
I created a custom log configuration for my Flask application:
```bash
sudo nano /etc/datadog-agent/conf.d/flask_app.d/conf.yaml
```

Add the following configuration:
```yaml
logs:
  - type: file
    path: /home/ubuntu/flask_app/app.log
    service: flask-app
    source: python
    sourcecategory: sourcecode
```

#### Restart Datadog Agent
```bash
sudo systemctl restart datadog-agent
```

#### Verification
After my configuration, the agent appeared in the Datadog dashboard under the "View Agents" section.

![Datadog View Agent Page](images/datadog_view_agent_page.png)

### Video Demo of My Work

https://github.com/user-attachments/assets/88b8c053-e4a3-4f5c-9ccc-03f9e1bfc7b7

## Challenges I Faced and How I Resolved Them

### Issue: Log Collection Not Working

**Problem I Encountered:**
Initially, logs from my Flask application were not appearing in the Datadog logs section. Upon investigation, I discovered the following error in the agent status:

```
Status: Error: cannot read file /home/ubuntu/flask_app/app.log: stat /home/ubuntu/flask_app/app.log: permission denied
```

**Root Cause:**
The Datadog agent didn't have the necessary permissions to read the log file. The agent runs under the `datadog-agent` user, which didn't have access to the user's home directory and the log file.

**How I Solved It:**
I fixed the permission issue by granting appropriate access to the Datadog agent:

```bash
# Grant execute permission on home directory for others
sudo chmod o+rx /home/ubuntu

# Grant execute permission on flask_app directory for others  
sudo chmod o+rx /home/ubuntu/flask_app

# Grant read permission on the log file for others
sudo chmod o+r /home/ubuntu/flask_app/app.log
```

**Command Explanations:**
- `chmod o+rx /home/ubuntu`: Grants read and execute permissions to "others" (including datadog-agent user) on the home directory
- `chmod o+rx /home/ubuntu/flask_app`: Grants read and execute permissions on the flask_app directory so the agent can navigate into it
- `chmod o+r /home/ubuntu/flask_app/app.log`: Grants read permission on the actual log file

After applying these permissions, restart the Datadog agent:
```bash
sudo systemctl restart datadog-agent
```

**Final Result:**
My permission fix successfully resolved the issue, and logs from the Flask application started appearing in the Datadog logs dashboard as expected.

## Key Skills and Technologies I Demonstrated

1. **AWS EC2 Management**: Successfully configured and managed cloud infrastructure including security groups and SSH access
2. **Linux System Administration**: Demonstrated proficiency in Ubuntu server management and file permissions
3. **Application Development**: Created a functional Flask web application with proper logging implementation
4. **Monitoring and Observability**: Successfully integrated enterprise-grade monitoring with Datadog
5. **Problem-Solving**: Diagnosed and resolved complex permission issues in Linux environments
6. **DevOps Best Practices**: Implemented end-to-end application deployment and monitoring pipeline

## What This Project Showcases

This assignment demonstrates my ability to:
- Work with cloud infrastructure (AWS EC2)
- Deploy and configure web applications
- Implement monitoring and logging solutions
- Troubleshoot system-level issues
- Follow security best practices
- Document technical processes comprehensively

## Project Files

- `app.py`: My Flask web application with custom logging implementation
- `flask-app-for-datadog.pem`: SSH key file I used for EC2 instance access
- `images/`: Complete visual documentation of my setup process
- `README.md`: This comprehensive documentation of my work

## Conclusion

I successfully completed this Datadog integration assignment, demonstrating my practical skills in cloud infrastructure, application deployment, and enterprise monitoring solutions. The project showcases my ability to work with industry-standard tools and resolve real-world technical challenges that arise during system implementation.
