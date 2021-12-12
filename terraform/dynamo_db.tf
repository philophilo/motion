resource "aws_dynamodb_table" "table" {
  name             = "${var.product}_${var.env_name}_users"
  hash_key         = "username"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "username"
    type = "S"
  }
}