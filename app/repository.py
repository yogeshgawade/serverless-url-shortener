import os

import boto3


if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )
else:
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="ap-south-1",
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )


table = dynamodb.Table(
    os.getenv("DYNAMODB_TABLE", "urls")
)


def save_url(code: str, url: str) -> None:
    table.put_item(
        Item={
            "code": code,
            "url": url,
        }
    )


def get_url(code: str) -> str | None:
    response = table.get_item(
        Key={"code": code}
    )

    item = response.get("Item")

    if item is None:
        return None

    return item["url"]
