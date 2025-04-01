import os
import json
import uuid
import boto3
from urllib.parse import urlencode
from botocore.config import Config


class StorageService:
    def __init__(self) -> None:
        self._bucket = os.environ.get("S3_BUCKET")
        config = Config(signature_version="v4")
        self._client = boto3.client("s3", config=config)

    def generate_signed_url(
        self, key: str, operation: str, audio_type="wav", session_id: str = None
    ):
        tags = {"session_id": uuid.uuid4()}

        if session_id != None:
            tags["session_id"] = session_id

        if operation == "put_object":
            tagging_str = None
            if tags:
                tagging_str = urlencode(tags)

            params = {
                "Bucket": self._bucket,
                "Key": key,
                "ContentType": f"audio/{audio_type}",
            }

            if tagging_str:
                params["Tagging"] = tagging_str

            return self._client.generate_presigned_url(
                "put_object",
                Params=params,
                ExpiresIn=900,
            )

        elif operation == "get_object":
            return self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=900,
            )

    def upload_file(self, key: str, file_path: str, tags: dict = None) -> None:
        self._client.upload_file(file_path, self._bucket, key, Tagging=urlencode(tags))

    def get_file(self, key: str) -> str:
        response = self._client.get_object(Bucket=self._bucket, Key=key)
        return json.loads(response["Body"].read().decode("utf-8"))

    def get_tags(self, key: str) -> dict[str, str]:
        response = self._client.get_object_tagging(Bucket=self._bucket, Key=key)
        return {tag["Key"]: tag["Value"] for tag in response.get("TagSet", [])}
