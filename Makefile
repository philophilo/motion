setup:
	@echo "Running docker-compose up"
	@docker-compose up -d
	@docker-compose exec lambda /bin/bash -c "cd /app && pip install -r /app/requirements.txt"

conf: setup
	@echo "Configuring AWS"
	@docker-compose exec lambda /app/script.sh configure

test: conf
	@docker-compose exec lambda /app/script.sh test

down:
	@docker-compose down

init:
	@docker-compose exec lambda /app/script.sh init

plan:
	@docker-compose exec lambda /app/script.sh plan

apply:
	@docker-compose exec lambda /app/script.sh apply

shell:
	@docker-compose exec lambda /bin/bash

output:
	@docker-compose exec lambda /app/script.sh output