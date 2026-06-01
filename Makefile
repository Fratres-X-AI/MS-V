.PHONY: reproduce install test ci

install:
	pip install -r requirements-lock.txt

reproduce:
	python -m sim.reproduce

validate:
	python -m sim.reproduce --validate-only

ci: reproduce
	python sim/validate_stress.py
	python sim/run_mega_suite.py --quick --workers 2

test: ci
