variable "env_name" {
  type = string
  validation {
    condition = anytrue([
      var.env_name == "prod",
      var.env_name == "staging",
      var.env_name == "test"
    ])
    error_message = "Environment must be one of prod, staging or test."
  }
}

variable "product" {
  type = string
}

variable "aws_region" {
  type = string
}
