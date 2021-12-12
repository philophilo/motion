output "base_url" {
  description = "Base URL for API Gateway stage."

  value = aws_apigatewayv2_stage.lambda_stage.invoke_url
}

resource "local_file" "base_url" {
    content  = aws_apigatewayv2_stage.lambda_stage.invoke_url
    filename = "url.txt"
}

resource "aws_s3_bucket_object" "base_url" {
    bucket     = aws_s3_bucket.bucket.id
    key = "url.txt"
    source = "url.txt"
    etag       = filemd5("url.txt")
    depends_on = [local_file.base_url]
}