.PHONY: one-pass reproduce install test ci lint mega report sobol audit figures all pull

one-pass:
	bash one_pass.sh 31 8192

pull:
	bash pull_from_pod.sh

install:
	pip install -r requirements-lock.txt ruff pytest

lint:
	ruff check sim models analysis tests

reproduce:
	python -m sim.reproduce

validate:
	python -m sim.reproduce --validate-only

test:
	pytest tests/ -q

sobol:
	python sim/run_sobol.py --n-base 8192 --workers 31
	python analysis/summarize_sobol.py
	python analysis/patch_assumption_register_sobol.py

mega:
	python sim/run_mega_suite.py --workers 31

report:
	python analysis/generate_verification_matrix.py
	python analysis/summarize_mega_suite.py
	python analysis/analyze_tail_risk.py
	python analysis/summarize_sobol.py

figures:
	python analysis/generate_figures.py
	python analysis/generate_form_factor_assets.py

form-factor:
	python analysis/generate_form_factor_assets.py

engineering-figures:
	python analysis/generate_engineering_drawings.py

renders3d:
	python analysis/generate_3d_renders.py

audit: lint test reproduce report figures

ci: reproduce
	python sim/validate_stress.py
	python sim/run_mega_suite.py --quick --workers 2 --out analysis/results/mega_suite_quick
	python sim/run_sobol.py --quick --workers 2
	python analysis/summarize_sobol.py
	python analysis/generate_verification_matrix.py
	pytest tests/ -q

all: ci
	@echo "Local CI complete. Full campaign: bash run_all.sh on RunPod"
