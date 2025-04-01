import uuid
from src.services.storage_service import StorageService
from src.helpers.lambda_payload import HttpRequest
from src.helpers.lambda_response import HttpResponse


def handler(event: HttpRequest, context: None) -> HttpResponse:
    storage_service = StorageService()
    file_id = uuid.uuid4()
    key = f"user_audios/request_{file_id}.wav"
    audio_type = "wav"
    session_id = uuid.uuid4()

    if "session_id" in event["queryStringParameters"]:
        session_id = event["queryStringParameters"]["session_id"]

    if (
        "key" in event["queryStringParameters"]
        and event["queryStringParameters"]["key"] != None
    ):
        object_key = event["queryStringParameters"]["key"]
        audio_type = object_key.split(".")[-1]
        key = f"ai_audios/{object_key}"

    operation = event["queryStringParameters"]["operation"]
    url = storage_service.generate_signed_url(
        key, operation, audio_type, str(session_id)
    )

    return HttpResponse(
        body={"url": url, "file_id": str(file_id), "session_id": str(session_id)}
    ).lambdaHttpResponse()
