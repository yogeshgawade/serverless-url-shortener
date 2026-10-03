resource "aws_apigatewayv2_api" "url_shortener" {
  name          = "url-shortener-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id = aws_apigatewayv2_api.url_shortener.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.url_shortener.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "shorten" {
  api_id    = aws_apigatewayv2_api.url_shortener.id
  route_key = "POST /shorten"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "redirect" {
  api_id    = aws_apigatewayv2_api.url_shortener.id
  route_key = "GET /{code}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.url_shortener.id
  name   = "$default"

  auto_deploy = true
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowApiGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.url_shortener.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.url_shortener.execution_arn}/*/*"
}
