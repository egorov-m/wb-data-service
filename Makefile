.PHONY: help
help:
		@echo "USAGE"
		@echo "    make <commands>"
		@echo ""
		@echo "AVAILABLE COMMANDS"
		@echo "up         Create and start containers in the background."
		@echo "down       Stop and remove containers, networks."
		@echo "export-dep Exporting poetry dependencies."

.PHONY: up
up:
		docker-compose -f docker-compose.yaml up -d

.PHONY: down
down:
		docker-compose -f docker-compose.yaml down

.PHONY: export-dep
export-dep:
		poetry export --without-hashes -f requirements.txt -o ./requirements.txt
