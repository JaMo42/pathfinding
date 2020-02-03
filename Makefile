mypy_opts := --ignore-missing-imports --show-error-codes
pycodestyle_opts := --ignore=E111,E114,E121,E125

sources := $(wildcard *.py) $(wildcard pathfinders/*.py)

run: main.py
	@python $^

help: main.py
	@python $^ --help

# Typecheck files
type-check: $(sources)
	mypy $(mypy_opts) $^

# Style check files
style-check: $(sources)
	pycodestyle $(pycodestyle_opts) $^
	@echo Success

# List available algorithms
list:
	@echo Implemented algorithms:
	@python -c "from pathfinders import algorithms; print(*algorithms.keys(), sep='\n')"
