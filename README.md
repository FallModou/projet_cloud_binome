#  Diabete Cloud Native Application  
### Docker • Docker Compose • Docker Swarm • Kubernetes • CI/CD

---

##  Description

Ce projet présente le déploiement d’une application backend de prédiction du diabète dans une architecture Cloud Native multi-environnements.

L’objectif est de mettre en œuvre :

- Docker (conteneurisation simple)
-  Docker Compose (orchestration locale multi-services)
-  Docker Swarm (orchestration cluster légère)
-  Kubernetes (orchestration avancée multi-nœuds)
-  CI/CD avec GitHub Actions


---

#  Architecture

##  Infrastructure Kubernetes

- 1 Master Node
- 2 Worker Nodes
- Réseau: 192.168.x.x
- Cluster initialisé avec kubeadm

##  CI/CD

GitHub → Self-Hosted Runner (Master VM) → DockerHub → Kubernetes Cluster

---
