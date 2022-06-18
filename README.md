# Python utils

Repo is intended to be a collection of python utils you can use

## Logging

Generic logging implemented based on decorators. Can pass in a description and logging level to influence the logging.

Functions decorated with the `@log[(description=, [level=])]]` decorator can have a `extra_logs` parameter which will be prefixed to the log message too

