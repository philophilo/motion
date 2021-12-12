resource "aws_lambda_function" "lambda_function" {
  function_name    = "first_function"
  s3_bucket        = "${var.product}-${var.env_name}-bucketxyz"
  s3_key           = "motion.zip"
  handler          = "motion.handler"
  runtime          = "python3.9"
  depends_on       = [aws_s3_bucket_object.zip]
  source_code_hash = data.archive_file.motion_app.output_base64sha256
  role             = aws_iam_role.lambda_role.arn

  environment {
    variables = {
      DB_TABLE_NAME = aws_dynamodb_table.table.name,
      REGION = var.aws_region
    }
  }
}
