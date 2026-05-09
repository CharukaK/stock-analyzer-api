PYTHON = python3
PIP = pip
VENV = .venv
BIN = $(VENV)/bin

install:
	@$(PYTHON) -m venv $(VENV)
	@$(BIN)/$(PIP) install --upgrade pip
	@$(BIN)/$(PIP) install -r requirements.txt

test: 
	@$(BIN)/pytest

create_db:
	@sqlite3 stock_analyzer.db < db/schema.sql
run-dev: create_db
	@fastapi dev

clean:
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
