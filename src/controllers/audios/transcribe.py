from src.helpers.lambda_payload import HttpRequest
from src.helpers.lambda_response import HttpResponse
from src.services.transcribe_audio_service import AudioTranscribeService


def handler(event: HttpRequest, context: None) -> HttpResponse:
    audio_file = event["Records"][0]["s3"]["object"]["key"]

    audio_transcribe_service = AudioTranscribeService(audio_file)
    audio_job_id = audio_transcribe_service.transcribe()

    return HttpResponse(
        body={"response": f"Success to start transcribe job with name {audio_job_id}!"}
    ).lambdaHttpResponse()
