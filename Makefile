.PHONY: help install run test clean docker-build docker-run docker-stop lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  run          Run the application"
	@echo "  test         Run tests"
	@echo "  clean        Clean up temporary files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker Compose"
	@echo "  docker-stop  Stop Docker containers"
	@echo "  lint         Run linting"
	@echo "  format       Format code"

# Install dependencies
install:
	pip install -r requirements.txt

# Run the application
run:
	python app.py

# Run tests
test:
	pytest tests/ -v

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

# Build Docker image
docker-build:
	docker build -t ai-travel-agent .

# Run with Docker Compose
docker-run:
	docker-compose up -d

# Stop Docker containers
docker-stop:
	docker-compose down

# Run linting
lint:
	flake8 app.py run_script.py
	mypy app.py

# Format code
format:
	black app.py run_script.py
	isort app.py run_script.py

# Development setup
dev-setup: install
	@echo "Creating .env file from example..."
	@if [ ! -f .env ]; then cp env.example .env; fi
	@echo "Development setup complete!"
	@echo "Please edit .env file with your API keys"

# Production setup
prod-setup: install
	@echo "Production setup complete!"
	@echo "Make sure to set environment variables for production"

# Check if .env exists
check-env:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found!"; \
		echo "Please copy env.example to .env and add your API keys"; \
		exit 1; \
	fi

# Run with environment check
run-safe: check-env run
