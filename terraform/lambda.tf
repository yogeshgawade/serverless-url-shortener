data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/.."
  output_path = "${path.module}/lambda.zip"

  excludes = [
    ".git",
    ".venv",
    "terraform",
    "tests",
    "local",
    "__pycache__",
    "*.pyc",
  ]
}

resource "aws_lambda_function" "url_shortener" {
  function_name = "url-shortener"
  role          = aws_iam_role.lambda.arn

  runtime = "python3.12"
  handler = "app.handler.lambda_handler"

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.urls.name
    }
  }
}
