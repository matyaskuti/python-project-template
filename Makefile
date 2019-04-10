.PHONY: install_lint_requirements
install_lint_requirements:
	pip3 install -e .[lint]

.PHONY: lint
lint: install_lint_requirements
	flake8 tests
	black --line-length=79 --check --diff tests
	pylint tests
	mypy tests

.PHONY: install_test_requirements
install_test_requirements:
	pip3 install -e .[test]

.PHONY: test
test: install_test_requirements
	pytest -s tests

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf python_project_template.egg-info
	find . -regex ".*__pycache__.*" -delete
	find . -regex "*.py[co]" -delete

.PHONY: format
format:
	black --line-length=79 tests
