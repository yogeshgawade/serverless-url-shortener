import secrets
import string
from urllib.parse import urlparse

from app.repository import save_url


CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits


def create_short_url(url: str) -> str:
    validate_url(url)

    code = generate_code()

    save_url(code, url)

    return code


def validate_url(url: str) -> None:
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Invalid URL")


def generate_code() -> str:
    return "".join(
        secrets.choice(ALPHABET)
        for _ in range(CODE_LENGTH)
    )
