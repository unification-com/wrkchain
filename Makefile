.DEFAULT_GOAL := help
.PHONY: sdk

# Set some variables
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "run: make sdk"

sdk:
	$(MAKE) init-prepare
	@mkdir -p `pwd`/build
	docker build -f Docker/sdk/sdk.Dockerfile -t sdk .
	docker run -v `pwd`/build:/build sdk

init-prepare:
	$(MAKE) info
	$(MAKE) clean

# Output some useful info
info:
	@echo "ROOT_DIR                      : $(ROOT_DIR)"

# Remove generated files and build env
clean:
	@rm -rf $(ROOT_DIR)/build
