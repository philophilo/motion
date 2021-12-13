[![CircleCI](https://circleci.com/gh/philophilo/motion.svg?style=shield)](https://app.circleci.com/pipelines/github/philophilo/motion?filter=all)

## Introduction

Terraform is used to deploy a lambda function to AWS. The lambda function uses AWS DynamoDB to store a username and password. Access to the lambda function is given through AWS API gateway.

The lambda function is in `app/` while the terraform code is in `terraform/`. The project uses `GNUMake` to orchestrate docker when developing locally. The CI tool used is CircleCI. Deployments are only made to the infrastructure when a pull request is merged to master. Other branches run test only. Terraform is run in a docker container for consistency in the development environments.

## Requirements

Ensure that the following are installed
```
- Docker
- GNUMake
```

### Setup

Clone the repository and create `.env` file in the root directory and add the following creadentials

```
git clone https://github.com/philophilo/motion.git
```

Required credentials

```
AWS_SECRET_KEY=" "
AWS_ACCESS_KEY=" "
REGION=" "
PRODUCT=" "
ENV_NAME=" "
DB_TABLE_NAME=" "
```

- `AWS_SECRET_KEY`, `AWS_ACCESS_KEY` and `REGION` are AWS key credentials, ensure that they are named appropriately! Such that `AWS_ACCESS_KEY` > `aws_access_key_id` and `aws_secret_access_key` > `AWS_SECRET_KEY`. The output has been defaulted to json. These are required for both the lambda function to run tests and terraform AWS provider to setup the terraform infrastructure plan

- `PRODUCT` is name of the application, this is custom. It is used in terraform to identify that resources belong to this particular application. However, it should not be too long as resource names have a character limit. This is only used by terraform.

- `ENV_NAME` This is the name of the of the environment. It can be one of `test`, `staging` or `prod`. The names are validated in [terraform/variables.tf](https://github.com/philophilo/motion/blob/master/terraform/variables.tf#L1-L11). This is only used by terraform.

- `DB_TABLE_NAME` is the name of the DynamDB created by terraform. It is required for both terraform and the lambda function.


### Running with make commands on a local machine

- `make setup` Builds the docker image `philophilo/py-tf-aws` which has terraform and AWS CLI installed. The command runs `docker-compose up` in detarched mode and then installs python requirements to run tests locally for the AWS lambda function.

- `make conf` Configures both Terraform and AWS. It creates `/root/aws` and `terraform/terraform.tfvars` in the docker container.

- `make test` Runs tests in `app/test_motion.py` using pytest and moto for mocking AWS resources. This command call both `make setup` and `make conf`, it is therefore not required to run the previous commands to run tests.

- `make down` Runs `docker-compose down` to stop the docker service

- `make init` Runs `terraform init` to initialize terraform. This will download the provider plugins that are required.

- `make plan` Runs `terraform plan`.

- `make apply` Runs `terraform apply`. It will require approval by typing `yes`. The circleci pipeline however [auto approves](https://github.com/philophilo/motion/blob/master/.circleci/config.yml#L61) the plan when running on [master](https://github.com/philophilo/motion/blob/master/.circleci/config.yml#L71-L77)

- `make shell` Allows opening the container's shell.

- `make output` This requires that `make apply` has been run already. It prints `base_url` from the api gateway and `bucket_name`.

- `make destroy` Destroys all the AWS resources that were setup usinf terraform.

### Continuous Integration (CI)

CircleCi is used as the CI tool. It is configured to run tests on the lambda function. The tests run on all branches. The deployment to AWS is run master after a merge from a pull request.

#### Accessing the Application

When Terraform is run from a local machine, the url will be in the terraform output as `base_url`

On the otherhand, if executed from the pipeline, circleci will send the url to the bucket `<product>-<env_name>-bucketxyz` in a file called `url.txt`. Download the file and access the link. Add a trailing slash `/` to the link in order to make api calls. `https://o5zaxoz6m6.execute-api.us-east-2.amazonaws.com/api/`

##### Example Test case

Register a User with POST method

`curl --header "Content-Type: application/json" -X "POST" --data '{"username":"xyz","password":"xyz"}' https://o5zaxoz6m6.execute-api.us-east-2.amazonaws.com/api/`

Get the user with GET method

`curl --header "Content-Type: application/json" -X "GET" --data '{"username":"xyz","password":"xyz"}' https://o5zaxoz6m6.execute-api.us-east-2.amazonaws.com/api/`

Using Postman of any other API platform

<img width="1254" alt="Screenshot 2021-12-12 at 17 28 06" src="https://user-images.githubusercontent.com/12629658/145717595-79fe4bf7-2336-4489-a889-ed62b7aa0c8d.png">