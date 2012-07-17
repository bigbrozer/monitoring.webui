# Makefile for reporting project
#
# Author: 	Monitoring & Reporting
# Creation: 17/07/2012
#

help:
	@echo "Available targets:"
	@echo "  * clean   -- Clean project (remove .pyc, swap vim files, etc...)"

## Cleaning
clean: clean-bytecode clean-backup

clean-bytecode:
	@echo 'Cleaning Python byte code files...'
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

clean-backup:
	@echo 'Cleaning backup files...'
	@find . -name '*~' -exec rm -f {} +
	@find . -name '#*#' -exec rm -f {} +

