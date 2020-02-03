mypy_opts :=
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
