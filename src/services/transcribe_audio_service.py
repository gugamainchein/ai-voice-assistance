import os
import boto3


class AudioTranscribeService:
    def __init__(self, audio_file_uri: str) -> None:
        self.bucket_name = os.environ.get("S3_BUCKET")
        self.audio_file_uri = f"s3://{self.bucket_name}/{audio_file_uri}"
        self.job_name = f"transcription-job-{audio_file_uri.replace("user_audios/request_", "").replace(".wav", "")}"
        self.transcribe_client = boto3.client("transcribe")
        self.s3_client = boto3.client("s3")

    def transcribe(self) -> str:
        self.transcribe_client.start_transcription_job(
            TranscriptionJobName=self.job_name,
            Media={"MediaFileUri": self.audio_file_uri},
            MediaFormat=self.audio_file_uri.split(".")[-1],
            LanguageCode="en-US",
            OutputBucketName=self.bucket_name,
            OutputKey="user_audios/",
        )

        return self.job_name
