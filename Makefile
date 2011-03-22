clean:
	@echo 'Cleaning Python byte code files...'
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	
	@echo 'Cleaning backup files...'
	@find . -name '*~' -exec rm -f {} +
	@find . -name '#*#' -exec rm -f {} +
