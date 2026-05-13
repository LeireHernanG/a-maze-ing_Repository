PYTHON = python3

PIP = pip

SCRIPT = a_maze_ing.py

all: install

install:
	$(PIP) install -r requirements.txt
run:
	$(PYTHON) main.py config.txt

debug:
	$(PYTHON) -m pdb $(SCRIPT)

lint:
	flake8 .  && \
	mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	flake8 . && \
	mypy --strict . 

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +  && rm -rf .mypy_cache

.PHONY:  clean all install run debug lint lint-strict