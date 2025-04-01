import os
import json
import boto3
from botocore.config import Config


class StorageService:
    def __init__(self) -> None:
        self._bucket = os.environ.get("S3_BUCKET")
        config = Config(signature_version="v4")
        self._client = boto3.client("s3", config=config)

    def generate_signed_url(self, key: str, operation: str, audio_type="wav"):
        if operation == "put_object":
            return self._client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": key,
                    "ContentType": f"audio/{audio_type}",
                },
                ExpiresIn=900,
            )
        elif operation == "get_object":
            return self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=900,
            )

    def upload_file(self, key: str, file_path: str) -> None:
        self._client.upload_file(file_path, self._bucket, key)

    def get_file(self, key: str) -> str:
        response = self._client.get_object(Bucket=self._bucket, Key=key)
        return json.loads(response["Body"].read().decode("utf-8"))
