terraform {
  backend "s3" {
    bucket = "philophilo-terraform"
    key    = "state/terraform.tfstate"
    region = "us-east-2"
  }
}