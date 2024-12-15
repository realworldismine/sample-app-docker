# sample-app-docker
## Prerequisite
### Install on EC2
- Refer to [userdata.sh](userdata.sh)
  - Install docker, docker-compose, java17, jenkins, git
  - Make swapfile 
- Modify and add the line in the `/etc/fstab`
```
/swapfile swap swap defaults 0 0
```
- Input a command as `sudo visudo` and add the line
```
jenkins ALL=(ALL)       NOPASSWD:ALL
```
- Input a command
```
sudo chmod 666 /var/run/docker.sock
```

### Jenkins Setting
- Make a credential for github in the Credential menu
- Check `Allow on Controller` and `Allow on Agents` in the Security menu
- Make sure `Jenkins URL` in the System menu
- Install plugins below (very important!!)
  - Amazon EC2, Ant, Docker, Docker Compose Build Step, Docker Pipeline, Email Extension, Github Integration, Gradle, JavaMail, LDAP, Matrix Authorization Strategy, Oracle JAVA SE Development Kit Installer, PAM Authentication, Pipeline, Pipeline Graph View, Pipeline: Github, Pipeline: Github Groovy Libraries, SSH Server, Timestamper, Workspace Cleanup
- Modify SMTP Email Environment Variables in the `Jenkinsfile`

## Implentation

### Python files
- Pre-provided microservice files
- Code additions and modifications were made for actual implementation
- Added and modified features:
  - Fixed some code errors
  - Added email sending functionality
  - Integrated Logger library
  - Integrated Prometheus Client library

### Directory creation
- Created empty directories to share the same space for logs and the database
- Connected during Docker Compose execution

### Dockerfile creation
- Installed and executed virtual environment (venv)
- Created and applied `requirements.txt` file
- No specific notes regarding the Dockerfile itself

### Docker Compose creation
#### Microservices
- Shared DB and log directories across each microservice
- Port mapping for each service
- Notification service uses sender information for email transmission, configured via ENV

#### cAdvisor
- A tool for collecting performance metrics of containers
- Port 8080 is reserved for Jenkins, so it is mapped to 8081

#### node-exporter
- A tool for collecting host performance metrics

#### prometheus
- Collects and manages performance data from cAdvisor and node-exporter
- Integrated with alertmanager to send email notifications upon anomalies
- Connects to cAdvisor, node-exporter, and alertmanager
- Specifies volume for `prometheus.yml` and `rules.yml` configuration files, sourced from the prometheus directory

#### alertmanager
- A program that triggers actual alerts based on Prometheus anomaly alerts
- In this system, it is implemented to send email notifications
- Specifies volume for the `alertmanager.yml` configuration file, sourced from the prometheus directory
- Configures sender information via ENV and includes replacement logic

#### grafana
- Visualizes the performance data aggregated by Prometheus
- Connects to Prometheus via `http://prometheus:9090`
- Imports Dashboard with ID 1860

#### Network
- All Docker containers are managed under a single Docker Network.

### Prometheus/AlertManager configuration files
#### `prometheus.yml` file
- Specifies rule files
- Configures alerting
- Creates separate jobs for each microservice and assigns labels, which are used in alertmanager
- Creates individual jobs for Prometheus, cAdvisor, and node-exporter

#### `rules.yml` file
- Defines alert rules for CPU usage, HTTP request latency, and container downtime
- Each rule is customizable and written with valid promQL functions

### `alertmanager.yml` file
- Configures email notifications
- Includes sender address information
- Password field left blank; email sending requires manual configuration and alertmanager restart
- Essentially a template file, dynamically replaced with ENV values during startup

## Process
- A Push Event occurs on the GitHub repository
- Jenkins polls via Webhook and triggers the Build process
- Upon build completion, Dockerfiles are generated, and containers are created and started using Docker Compose
- Postman is used to verify API calls after startup
- Logs and alerts are checked
- Dashboard visualization is verified using Grafana 



