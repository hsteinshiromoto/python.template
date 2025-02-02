SHELL:=/bin/bash
.DEFAULT_GOAL := help
.PHONY: help docs

# ---
# Variables
# ---
PROJECT_PATH := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
GIT_REMOTE=$(shell basename $(shell git remote get-url origin))
PROJECT_NAME=$(shell echo $(GIT_REMOTE:.git=))
CURRENT_VERSION=$(shell git tag -l --sort=-creatordate | head -n 1 | cut -d "v" -f2-)

DOCKER_REPOSITORY=ghcr.io
DOCKER_IMAGE_NAME=${DOCKER_REPOSITORY}/hsteinshiromoto/${PROJECT_NAME}/${PROJECT_NAME}
DOCKER_TAG=$(shell git ls-files -s Dockerfile | awk '{print $$2}' | cut -c1-16)
DOCKER_PARENT_IMAGE=debian:latest

BUILD_DATE = $(shell date +%Y%m%d-%H:%M:%S)
PYTHON_VERSION="3.11.1"

# ---
# Sphix documentation settings
# ---
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = template.py
SOURCEDIR     = docs/src
BUILDDIR      = docs

# ---
# Commands
# ---
temp:
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE_NAME}:${DOCKER_TAG})

	@echo ${DOCKER_IMAGE_TAG}


## Build Python package
build:
	poetry build

## Check package build
check:
	twine check dist/*

## Publish to PyPI
publish: 
	poetry publish --username __token__ --password $PYPI_API_TOKEN

## Git hooks
hooks:
	cp bin/post-checkout .git/hooks/post-checkout

## Build Docker app image
image:
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE_NAME}:${DOCKER_TAG})

	@echo "Building docker image ${DOCKER_IMAGE_TAG}"
	docker build --build-arg BUILD_DATE=${BUILD_DATE} \
				--build-arg DOCKER_PARENT_IMAGE=${DOCKER_PARENT_IMAGE} \
				--build-arg PROJECT_NAME=${PROJECT_NAME} \
				--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
				-t ${DOCKER_IMAGE_TAG} .
	@echo "Done"

## Sphinx documentation
docs:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -r docs/html/* docs/ && rm -R docs/html
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

## Pull latest image from repository
pull:
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE_NAME}:${DOCKER_TAG})

	docker pull ${DOCKER_IMAGE_TAG}

# ---
# Self Documenting Commands
# ---

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
