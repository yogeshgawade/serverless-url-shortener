import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="ap-south-1",
    aws_access_key_id="local",
    aws_secret_access_key="local",
)

existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

if "urls" not in existing_tables:
    table = dynamodb.create_table(
        TableName="urls",
        KeySchema=[
            {"AttributeName": "code", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "code", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    table.wait_until_exists()
    print("Created DynamoDB table: urls")
else:
    print("DynamoDB table already exists: urls")
