import json
from src.helpers.lambda_payload import HttpRequest
from src.helpers.lambda_response import HttpResponse
from src.services.storage_service import StorageService
from src.services.audio_response_service import AudioResponseService
from src.services.process_user_request_service import ProcessUserRequestService


def handler(event: HttpRequest, context: None) -> HttpResponse:
    audio_file = event["Records"][0]["s3"]["object"]["key"]

    storage_service = StorageService()
    audio_user_text = storage_service.get_file(audio_file)
    audio_user_text = audio_user_text["results"]["transcripts"][0]["transcript"]

    process_user_request_service = ProcessUserRequestService(audio_user_text)
    answer_to_user = process_user_request_service.process_response()

    audio_response_service = AudioResponseService(answer_to_user)
    polly_audio_url = audio_response_service.audio_response_by_polly()

    audio_name = audio_file.replace("transcription-job-", "")
    audio_name = audio_name.replace(".json", ".mp3")
    audio_name = audio_name.replace("user_audios/", "ai_audios/response_")
    storage_service.upload_file(audio_name, polly_audio_url.get("audio_url"))

    return HttpResponse(
        body={"response": "Success to generate audio response!"}
    ).lambdaHttpResponse()
