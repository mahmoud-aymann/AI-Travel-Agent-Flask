# Deployment Guide

This guide covers various deployment options for the AI Travel Agent application.

## Table of Contents
##
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)
- [Environment Configuration](#environment-configuration)
- [Monitoring and Logging](#monitoring-and-logging)

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd ai-travel-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your API keys

# Run the application
python app.py
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ai-travel-agent

# Set up environment variables
cp env.example .env
# Edit .env with your API keys

# Run with Docker Compose
docker-compose up -d
```

### Using Docker directly

```bash
# Build the image
docker build -t ai-travel-agent .

# Run the container
docker run -d \
  --name ai-travel-agent \
  -p 5000:5000 \
  --env-file .env \
  ai-travel-agent
```

### Production with Nginx

```bash
# Run with Nginx reverse proxy
docker-compose --profile production up -d
```

## Cloud Deployment

### Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set SERPER_API_KEY=your_key
   heroku config:set OPENWEATHERMAP_API_KEY=your_key
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### AWS (Elastic Beanstalk)

1. **Install EB CLI**
2. **Initialize EB application**
   ```bash
   eb init
   eb create production
   ```

3. **Set environment variables**
   ```bash
   eb setenv OPENAI_API_KEY=your_key
   eb setenv SERPER_API_KEY=your_key
   eb setenv OPENWEATHERMAP_API_KEY=your_key
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

### Google Cloud Platform

1. **Install gcloud CLI**
2. **Create app.yaml**
   ```yaml
   runtime: python39
   env_variables:
     OPENAI_API_KEY: "your_key"
     SERPER_API_KEY: "your_key"
     OPENWEATHERMAP_API_KEY: "your_key"
   ```

3. **Deploy**
   ```bash
   gcloud app deploy
   ```

### DigitalOcean (App Platform)

1. **Create app specification**
2. **Set environment variables**
3. **Deploy from GitHub**

## Production Considerations

### Security

- **Use HTTPS**: Always use HTTPS in production
- **Environment Variables**: Never commit API keys to version control
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Input Validation**: Validate all user inputs
- **CORS**: Configure CORS properly

### Performance

- **WSGI Server**: Use Gunicorn or uWSGI instead of Flask dev server
- **Reverse Proxy**: Use Nginx or Apache as reverse proxy
- **Caching**: Implement Redis or Memcached for caching
- **CDN**: Use CDN for static files
- **Database**: Use PostgreSQL for production data

### Monitoring

- **Health Checks**: Implement health check endpoints
- **Logging**: Set up proper logging
- **Metrics**: Monitor application metrics
- **Alerts**: Set up alerts for critical issues

## Environment Configuration

### Required Variables

```env
# OpenAI API (Required)
OPENAI_API_KEY=sk-your-key-here

# Optional APIs
SERPER_API_KEY=your-serper-key
OPENWEATHERMAP_API_KEY=your-weather-key

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key
```

### Optional Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Security
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT=1000
```

## Monitoring and Logging

### Health Checks

The application provides health check endpoints:

- `GET /api/status` - API status
- `GET /health` - Application health

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### Metrics Collection

Consider using:
- **Prometheus** for metrics collection
- **Grafana** for visualization
- **ELK Stack** for log analysis

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 <PID>
   ```

2. **Environment variables not loaded**
   - Check `.env` file exists
   - Verify variable names are correct
   - Restart the application

3. **API key errors**
   - Verify API keys are valid
   - Check API quotas and billing
   - Test API keys independently

### Debug Mode

For debugging, set:
```env
FLASK_DEBUG=True
FLASK_ENV=development
```

## Support

For deployment issues:
- Check the [troubleshooting section](#troubleshooting)
- Review the [GitHub issues](https://github.com/yourusername/ai-travel-agent/issues)
- Contact support at support@aitravelagent.com

---

**Last Updated**: October 11, 2025
