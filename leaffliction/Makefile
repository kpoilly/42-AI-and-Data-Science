SHELL := /bin/bash
python := python3
SRC_DIR := .
VENV_DIR := leaf_venv
DEP_FILE := requirements.txt

# The URL to the dataset
ASSET_URL := https://cdn.intra.42.fr/document/document/17547/leaves.zip
DATA_DIR := data

DOCKER_IMG_NAME := postgres-img
DOCKER_CONTAINER_NAME := postgres-container

define venvWrapper
	{\
	. $(VENV_DIR)/bin/activate; \
	$1; \
	}
endef

APP_FILE := manage.py

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  start:    	 Run the project"
	@echo "  install:    Install the project"
	@echo "  freeze:     Freeze the dependencies"
	@echo "  fclean:     Remove the virtual environment and the datasets"
	@echo "  clean:      Remove the cache files"
	@echo "  re:         Reinstall the project"
	@echo "  phony:      Run the phony targets"

start:
	@$(call venvWrapper, streamlit run main.py )

run-docker:
	docker build -t $(DOCKER_IMG_NAME) .
	docker run -d --name $(DOCKER_CONTAINER_NAME) -p 5432:5432 $(DOCKER_IMG_NAME)

prune-docker:
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)
	docker rmi $(DOCKER_IMG_NAME)

install:
		@{ \
		echo "Setting up..."; \
		if [ -z ${ASSET_URL} ] || [ -d ${DATA_DIR} ]; then echo "nothing to download"; else \
			filename=$(notdir ${ASSET_URL}); \
			wget --no-check-certificate -O $${filename} ${ASSET_URL}; \
			mkdir -p ${DATA_DIR}/; \
			if [[ $${filename} == *.zip ]]; then \
				echo "Unzipping..."; \
				unzip -o $${filename} -d ${DATA_DIR}/; \
			elif [[ $${filename} == *.tar || $${filename} == *.tar.gz || $${filename} == *.tgz ]]; then \
				echo "Untarring..."; \
				tar -xvf $${filename} -C ${DATA_DIR}/; \
			rm -rf $${filename}; \
			fi; \
		fi; \
		python3 -m venv ${VENV_DIR}; \
		. ${VENV_DIR}/bin/activate; \
		if [ -f ${DEP_FILE}  ]; then \
			pip install -r ${DEP_FILE}; \
			echo "Installing dependencies...DONE"; \
		fi; \
		}

freeze:
	$(call venvWrapper, pip freeze > ${DEP_FILE})

fclean: clean
	rm -rf bin/ include/ lib/ lib64 pyvenv.cfg share/ etc/ $(VENV_DIR)

clean:
	rm -rf ${SRC_DIR}/__pycache__ */**/**/__pycache__ */**/__pycache__ */__pycache__

re: fclean install

phony: install freeze fclean clean re help