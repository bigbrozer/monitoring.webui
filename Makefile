# Cleaning stuff
clean: clean-python clean-backup clean-log

clean-python:
	@echo 'Cleaning Python byte code files...'
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

clean-backup:
	@echo 'Cleaning backup files...'
	@find . -name '*~' -exec rm -f {} +
	@find . -name '*.swp' -exec rm -f {} +
	@find . -name '#*#' -exec rm -f {} +

clean-log:
	@echo 'Cleaning log files...'
	@find log/ -name '*.log' -exec rm -f {} +