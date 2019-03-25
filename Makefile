.DEFAULT_GOAL := help
.PHONY: clean help info init-prepare sdk

# Set some variables
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
HOST_UID=$(shell id -u)

ifndef BUILD_DIR
    BUILD_DIR:=build
endif

help:
	@echo "Create and edit $(ROOT_DIR)/wrkchain.json"
	@echo "then run:"
	@echo "  make sdk"

sdk:
	$(MAKE) init-prepare
	@mkdir -p `pwd`/$(BUILD_DIR)
	docker build -f Docker/sdk/sdk.Dockerfile --build-arg HOST_UID=$(HOST_UID) -t sdk .
	docker run -v `pwd`/$(BUILD_DIR):/home/sdkuser/build -e HOST_UID=$(HOST_UID) sdk

init-prepare:
	$(MAKE) check-config
	$(MAKE) info
	$(MAKE) clean

# Output some useful info
info:
	@echo "ROOT_DIR      : $(ROOT_DIR)"
	@echo "BUILD_DIR     : $(BUILD_DIR)"
	@echo "HOST_UID      : $(HOST_UID)"

# Remove generated files and build env
clean:
	@rm -rf $(ROOT_DIR)/$(BUILD_DIR)

check-config:
	@test -s $(ROOT_DIR)/wrkchain.json || { echo "\nBUILD ERROR!\n\nwrkchain.json does not exist. Exiting...\n"; exit 1; }
