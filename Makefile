sample = 01
mode = mode_1
action = action_1
run-sample:
	PYTHONPATH=$${PYTHONPATH}:$${PWD} python3 arg_parse/_samples/_$(sample)/run.py $(mode) $(action) --required-arg a

install:
	pip install .