PYTHON = python3
PIP = pip
VENV = venv
BIN = $(VENV)/bin

install:
	@$(PYTHON) -m venv $(VENV)
	@$(BIN)/$(PIP) install --upgrade pip
	@$(BIN)/$(PIP) install -r requirements.txt

test: 
	@$(BIN)/pytest

run:
	@$(BIN)/python main.py

clean:
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
