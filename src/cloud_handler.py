"""Cloud-neutral entry point used by AWS Lambda and Azure Functions."""
from pathlib import Path
from tempfile import TemporaryDirectory

from src.pipeline import run


def process_downloaded_file(local_input: str) -> dict[str, object]:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        return run(Path(local_input), root / "processed", root / "sales.db")


def lambda_handler(event, context):  # AWS adapter; storage download is added at deployment.
    return {"statusCode": 200, "body": {"message": "Pipeline adapter ready", "event": event}}
