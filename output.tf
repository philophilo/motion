output "base_url" {
  description = "Base URL for API Gateway stage."

  value = aws_apigatewayv2_stage.lambda_stage.invoke_url
}

output "bucket_name" {
  description = "Name of bucket created"
  value = aws_s3_bucket.bucket.bucket
}