import uuid
import boto3
import base64


class AudioResponseService:
    def __init__(self, answer_to_user: str) -> None:
        self.polly_client = boto3.client("polly")
        self.answer_to_user = answer_to_user

    def audio_response_by_polly(self) -> str:
        speech = self.polly_client.synthesize_speech(
            Engine="generative",
            Text=self.answer_to_user,
            OutputFormat="mp3",
            VoiceId="Ruth",
        )

        if "AudioStream" in speech:
            audio_data = base64.b64encode(speech["AudioStream"].read()).decode("utf-8")
            audio_name = uuid.uuid4()
            audio_url = f"/tmp/{audio_name}.mp3"

            with open(audio_url, "wb") as f:
                f.write(base64.b64decode(audio_data))

            return {"audio_url": audio_url, "audio_name": str(audio_name)}
