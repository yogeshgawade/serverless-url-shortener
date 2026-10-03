output "dynamodb_table_name" {
  value = aws_dynamodb_table.urls.name
}

output "lambda_function_name" {
  value = aws_lambda_function.url_shortener.function_name
}

output "api_url" {
  value = aws_apigatewayv2_api.url_shortener.api_endpoint
}
