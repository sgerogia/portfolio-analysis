.PHONY: install test


install:
	@echo "Creating virtual environment and installing dependencies..."
	python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt;

analyse:
	@echo "Analysing portfolio..."
	. venv/bin/activate && \
    python3 ./scripts/main.py;
