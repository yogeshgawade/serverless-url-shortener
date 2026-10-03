resource "aws_dynamodb_table" "urls" {
  name         = "url-shortener-urls"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "code"

  attribute {
    name = "code"
    type = "S"
  }
}
