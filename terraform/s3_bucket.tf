resource "aws_s3_bucket" "bucket" {
  bucket        = "${var.product}-${var.env_name}-bucketxyz"
  force_destroy = true
}