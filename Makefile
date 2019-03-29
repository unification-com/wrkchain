.DEFAULT_GOAL := help
.PHONY: clean help info init-prepare sdk

# Set some variables
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
HOST_UID=$(shell id -u)
HOST_GID=$(shell id -g)

ifndef BUILD_DIR
    BUILD_DIR:=build
endif

sdk:
	$(MAKE) init-prepare
	@mkdir -p `pwd`/$(BUILD_DIR)
	docker build -f Docker/sdk/sdk.Dockerfile --build-arg HOST_UID=$(HOST_UID) --build-arg HOST_GID=$(HOST_GID) -t sdk .
	docker run -v `pwd`/$(BUILD_DIR):/home/sdkuser/build --env HOST_UID=$(HOST_UID) --env HOST_BUILD_DIR=$(BUILD_DIR) sdk

init-prepare:
	$(MAKE) check-config
	$(MAKE) info
	$(MAKE) clean

# Output some useful info
info:
	@echo "ROOT_DIR      : $(ROOT_DIR)"
	@echo "BUILD_DIR     : $(BUILD_DIR)"
	@echo "HOST_UID      : $(HOST_UID)"
	@echo "HOST_GID      : $(HOST_GID)"

# Remove generated files and build env
clean:
	@rm -rf $(ROOT_DIR)/$(BUILD_DIR)

check-config:
	@test -s $(ROOT_DIR)/wrkchain.json || { echo "\nBUILD ERROR!\n\nwrkchain.json does not exist. Exiting...\n"; exit 1; }

help:
	@echo "Create and edit $(ROOT_DIR)/wrkchain.json"
	@echo "then run:"
	@echo ""
	@echo "  make sdk"
	@echo ""
	@echo "Build path can also be specified by setting BUILD_DIR"
	@echo "BUILD_DIR must be a relative path. Examples:"
	@echo ""
	@echo "  BUILD_DIR=../build make sdk"
	@echo "  BUILD_DIR=./build_test make sdk"
	@echo "  BUILD_DIR=build_another make sdk"
	@echo ""
