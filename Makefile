# COLORS
GREEN := $(shell tput -Txterm setaf 2)
WHITE := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
CYAN := $(shell tput -Txterm setaf 6)
RESET := $(shell tput -Txterm sgr0)

HELP_FUN = \
	%help; \
	while(<>) { \
			if(/^([a-z0-9_-]+):.*\#\#(?:@(\w+))?\s(.*)$$/) { \
					push(@{$$help{$$2}}, [$$1, $$3]); \
			} \
	}; \
	print "usage: make [target]\n\n"; \
	for (sort keys %help) { \
		print "${WHITE}$$_:${RESET}\n"; \
		for (@{$$help{$$_}}) { \
			$$sep = " " x (32 - length $$_->[0]); \
			print "  ${CYAN}$$_->[0]${RESET}$$sep${RESET}$$_->[1]\n"; \
		}; \
		print "\n"; \
	}

.PHONY: help

help: ##@help print help
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

help-python: ##@help print help from python
	@python main.py -h

encrypt: ##@mimiqui encrypt data in the picture
	@echo "${YELLOW}> encrypt data in image...${RESET}"
	@python main.py --encrypt --data-file index.txt --image-file index.png --image-output encrypted.png --key allocine --size 16
	@echo "${GREEN}✓ Wonderful! Your picture is ready in output.png${RESET}"

decrypt: ##@mimiqui decrypt data in the picture
	@echo "${YELLOW}> decrypt data in image...${RESET}"
	@python main.py --decrypt --image-file encrypted.png --data-output output --key allocine --size 16
	@echo "${GREEN}✓ Wonderful! Your data is ready in output file${RESET}"
