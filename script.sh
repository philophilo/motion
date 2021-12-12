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
    cd /app/app
    pytest
}

configure_terraform() {
    cd /app/terraform
    echo "env_name   = \"$ENV_NAME\"" >> terraform.tfvar
    echo "product    = \"$PRODUCT\"" >> terraform.tfvar
    echo "aws_region = \"$AWS_REGION\"" >> terraform.tfvar
}

terraform_init() {
    cd /app/terraform
    terraform init
}

terraform_plan() {
    cd /app/terraform
    terraform plan
}

terraform_apply() {
    cd /app/terraform
    terraform apply
}

if [[ $1 == "configure" ]];
then
    configure_aws
    configure_terraform
elif [[ $1 == "test" ]];
then
    run_tests
elif [[ $1 == "init" ]];
then
    terraform_init
elif [[ $1 == "plan" ]];
then
    terraform_plan
elif [[ $1 == "apply" ]];
then
    terraform_apply
fi
