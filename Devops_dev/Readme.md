DevOps Monitoring project

Project Goal --

The goal of this project is to demonstrate a production-style DevOps CI/CD pipeline that automatically builds, deploys, and monitors a containerized Python application using cloud-native tools.

Developer Code → Docker Image → Container Registry → Kubernetes Deployment → Monitoring

Project Structure --
Observe/
│
├── Devops_dev/
│   │
│   └── README.md
│   ├── app/
│   │   ├── main.py
│   │   └── requirements.txt
│   │
│   ├── docker/
│   │   └── Dockerfile
│   │
│   └── kubernetes/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── monitoring/
│           ├── prometheus.yaml
│           └── grafana.yaml
│
├── .github/
   └── workflows/
       └── deployment.yml




