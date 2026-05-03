PYTHON_VERSION = python3
MAIN_FILE = a_maze_ing.py
CONFIG_FILE = config.txt

install:
	$(PYTHON_VERSION) -m pip install -r requirements.txt

run:
	$(PYTHON_VERSION) $(MAIN_FILE) $(CONFIG_FILE)

debug:
	$(PYTHON_VERSION) -m pdb $(MAIN_FILE) $(CONFIG_FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
