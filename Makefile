args =
sample = 01
mode = mode_1
action = action_1
run-sample:
	PYTHONPATH=$${PYTHONPATH}:$${PWD} python3 arg_parse/_samples/_$(sample)/run.py $(mode) $(action) --required-arg 1 $(args)

# Install locally via pip.
install:
	pip install .

# Uninstall.
uninstall:
	pip uninstall arg_parse

# Clean coverage data.
clean-coverage:
	rm -rf htmlcov .coverage

# Clean pip build files.
clean-build:
	rm -rf build
	rm -rf *.egg-info

# Run test-suite.
# Use args="-k some_test" to match a regex test range.
# Display coverage in browser at: ./htmlcov/index.html
test_logging_level = info
args = ""
run-test:
	bash -c "pytest-3 test --cov=arg_parse --cov-report=html $(args)"
run-test-verbose:
	bash -c "pytest-3 test --cov=arg_parse --cov-report=html -vs --log-cli-level=$(test_logging_level) $(args)"

# Show coverage data from testing.
show-coverage:
	firefox ./htmlcov/index.html