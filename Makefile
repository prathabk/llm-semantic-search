.PHONY: help install run test clean setup-typesense setup-ollama

help:
	@echo "Available commands:"
	@echo "  make install          - Install Python dependencies"
	@echo "  make run             - Run the Flask application"
	@echo "  make test            - Run tests"
	@echo "  make clean           - Remove temporary files"
	@echo "  make setup-typesense - Instructions for Typesense setup"
	@echo "  make setup-ollama    - Instructions for Ollama setup"

install:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	@echo "✅ Dependencies installed"

run:
	@echo "Starting Flask server on http://localhost:9010"
	./venv/bin/python app.py

test:
	@echo "Running tests..."
	./venv/bin/python test_demo.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ Cleaned temporary files"

setup-typesense:
	@echo "===================================="
	@echo "Typesense Setup Instructions"
	@echo "===================================="
	@echo ""
	@echo "Option 1: Docker (Recommended)"
	@echo "  docker run -d -p 8108:8108 -v \$$(pwd)/typesense-data:/data \\"
	@echo "    typesense/typesense:27.1 --data-dir /data \\"
	@echo "    --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se --enable-cors"
	@echo ""
	@echo "Option 2: Homebrew (macOS)"
	@echo "  brew install typesense-server"
	@echo "  typesense-server --data-dir=/tmp/typesense-data --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se"
	@echo ""
	@echo "Verify: curl http://localhost:8108/health"

setup-ollama:
	@echo "===================================="
	@echo "Ollama Setup Instructions"
	@echo "===================================="
	@echo ""
	@echo "Installation:"
	@echo "  curl -fsSL https://ollama.ai/install.sh | sh"
	@echo ""
	@echo "Pull Models:"
	@echo "  ollama pull gemma3:1b"
	@echo ""
	@echo "Verify: ollama list"
