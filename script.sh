#! /bin/bash

configure_aws() {
    cd ~/
    mkdir -p ~/.aws
    echo "[default]" > ~/.aws/credentials
    echo "aws_access_key_id = $AWS_ACCESS_KEY" >> ~/.aws/credentials
    echo "aws_secret_access_key = $AWS_SECRET_KEY" >> ~/.aws/credentials

    echo "[default]" > ~/.aws/config
    echo "region = $AWS_REGION" >> ~/.aws/config
    echo "output = json" >> ~/.aws/config

    chmod 600 ~/.aws/config ~/.aws/credentials
}

run_tests() {
    cd /app
    pytest
}

configure_terraform() {
    cd /app
    echo "env_name   = \"$ENV_NAME\"" >> terraform.tfvar
    echo "product    = \"$PRODUCT\"" >> terraform.tfvar
    echo "aws_region = \"$AWS_REGION\"" >> terraform.tfvar
}

terraform_plan() {
    cd /app
    terraform_plan
}

terraform_apply() {
    yes|terraform terraform_apply
}

if [[ $1 == "configure_aws" ]];
then
    configure_aws
elif [[ $1 == "configure_terraform" ]];
then
    configure_terraform
elif [[ $1 == "test" ]];
then
    run_tests
fi
