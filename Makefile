setup:
	@echo "Running docker-compose up"
	@docker-compose up -d
	@docker-compose exec lambda /bin/bash -c "cd /app && pip install -r /app/requirements.txt"

aws: setup
	@echo "Configuring AWS"
	@docker-compose exec lambda /app/script.sh configure_aws

test: aws
	@docker-compose exec lambda /app/script.sh test

down:
	@docker-compose down