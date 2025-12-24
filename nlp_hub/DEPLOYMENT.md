"""
Deployment Guide for NLP Hub

Complete guide for deploying NLP Hub to production environments.

Author: Yacine-ai-tech (siddoyacinetech227@gmail.com)
Repository: https://github.com/Yacine-ai-tech/my_NLP_Journey
Last Updated: December 24, 2025
"""

# Deployment Guide

## Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] All tests passing
- [ ] Code reviewed
- [ ] API documentation up-to-date
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Security audit completed

## Local Deployment

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Run application
python main.py

# 4. Access API
# Navigate to http://localhost:8000/docs
```

## Docker Deployment

```bash
# 1. Build image
docker build -f docker/Dockerfile -t nlp-hub:latest .

# 2. Run container
docker run -p 8000:8000 \
  -e LLM_API_KEY=your_key \
  -e ENVIRONMENT=production \
  nlp-hub:latest

# 3. Run with Docker Compose
docker-compose -f docker/docker-compose.yml up -d
```

## Cloud Deployment

### AWS

```bash
# Using ECR and ECS
aws ecr create-repository --repository-name nlp-hub
docker tag nlp-hub:latest {account}.dkr.ecr.{region}.amazonaws.com/nlp-hub:latest
docker push {account}.dkr.ecr.{region}.amazonaws.com/nlp-hub:latest
```

### Google Cloud

```bash
# Using Cloud Run
gcloud run deploy nlp-hub \
  --image gcr.io/{project}/nlp-hub:latest \
  --platform managed
```

### Azure

```bash
# Using Container Instances
az container create \
  --resource-group myGroup \
  --name nlp-hub \
  --image nlp-hub:latest
```

## Database Setup

### PostgreSQL

```bash
# Create user and database
sudo -u postgres createuser nlp_hub
sudo -u postgres createdb -O nlp_hub nlp_hub

# Initialize schema
python scripts/init_db.py
```

## Monitoring & Logging

### Application Logs

```bash
# View logs
tail -f logs/app.log

# Filter logs
grep "ERROR" logs/app.log | jq .
```

### Performance Monitoring

Monitor these metrics:
- API response time
- LLM token usage
- Vector DB query time
- Memory usage
- CPU usage

## Backup Strategy

```bash
# Backup PostgreSQL
pg_dump nlp_hub > backup.sql

# Backup FAISS indices
cp -r data/embeddings/vectors backup/

# Backup model checkpoints
cp -r models/checkpoints backup/
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml with scaling
services:
  nlp-hub-api:
    deploy:
      replicas: 3
    environment:
      - WORKERS=4
```

### Resource Limits

```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

## Post-Deployment

1. Run smoke tests
2. Monitor error rates
3. Check API response times
4. Verify database connectivity
5. Test critical workflows

---

For production support, contact: ops@nlphub.com
