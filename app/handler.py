import json

from app.repository import get_url
from app.service import create_short_url


def lambda_handler(event, context):
    method = event.get("httpMethod")

    if method == "POST":
        return shorten(event)

    if method == "GET":
        return redirect(event)

    return response(
        405,
        {"error": "Method not allowed"},
    )


def shorten(event):
    try:
        body = json.loads(event.get("body") or "{}")
        url = body.get("url")

        if not url:
            return response(
                400,
                {"error": "url is required"},
            )

        code = create_short_url(url)

        return response(
            201,
            {"code": code},
        )

    except ValueError as e:
        return response(
            400,
            {"error": str(e)},
        )

    except Exception:
        return response(
            500,
            {"error": "Internal server error"},
        )


def redirect(event):
    path_parameters = event.get("pathParameters") or {}
    code = path_parameters.get("code")

    if not code:
        return response(
            400,
            {"error": "code is required"},
        )

    url = get_url(code)

    if url is None:
        return response(
            404,
            {"error": "Short URL not found"},
        )

    return {
        "statusCode": 302,
        "headers": {
            "Location": url,
        },
        "body": "",
    }


def response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }
