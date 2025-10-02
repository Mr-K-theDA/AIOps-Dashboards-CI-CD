# Simple pipeline Makefile

.PHONY: all check_reqs test build_docker smoke pipeline

all: check_reqs pipeline

check_reqs:
	@echo "Checking requirements..."
	@command -v python > /dev/null 2>&1 || (echo "Python not found" && exit 1)
	@command -v docker > /dev/null 2>&1 || (echo "Docker not found" && exit 1)
	@command -v git > /dev/null 2>&1 || (echo "Git not found" && exit 1)
	@test -f .env || (echo ".env file missing" && exit 1)
	@test -f requirements.txt && python -m pip install -q -r requirements.txt || (echo "Failed to install requirements" && exit 1)
	@mkdir -p logs
	@echo "Requirements check passed."

pipeline: test build_docker smoke
	@python capture_logs.py
	@python post_pipeline.py
	@echo "Pipeline completed."

# Run tests

test:
	@echo "Running tests..."
	@python -m unittest discover > logs/test.log 2>&1
	@echo $$? > logs/test.exit

# Build Docker image

build_docker:
	@echo "Building Docker image..."
	@docker build -t myapp . > logs/build_docker.log 2>&1
	@echo $$? > logs/build_docker.exit

# Smoke test

smoke:
	@echo "Running smoke tests..."
	@python smoke_test.py > logs/smoke.log 2>&1
	@echo $$? > logs/smoke.exit
