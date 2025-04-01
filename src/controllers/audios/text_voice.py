from src.helpers.lambda_payload import HttpRequest
from src.helpers.lambda_response import HttpResponse
from src.services.storage_service import StorageService
from src.services.audio_response_service import AudioResponseService
from src.repository.conversation_repository import ConversationRepository
from src.services.process_user_request_service import ProcessUserRequestService


def handler(event: HttpRequest, context: None) -> HttpResponse:
    audio_file = event["Records"][0]["s3"]["object"]["key"]

    storage_service = StorageService()
    tags = storage_service.get_tags(
        audio_file.replace(".json", ".wav").replace("transcription-job-", "request_")
    )

    audio_name = audio_file.replace("transcription-job-", "")
    audio_name = audio_name.replace(".json", ".mp3")
    audio_name = audio_name.replace("user_audios/", "ai_audios/response_")

    conversation_repository = ConversationRepository()

    audio_user_text = storage_service.get_file(audio_file)
    audio_user_text = audio_user_text["results"]["transcripts"][0]["transcript"]

    conversation_repository.load_data_on_conversation_table(
        session_id=tags.get("session_id"),
        message_id=audio_name.replace("ai_audios/response_", "request_"),
        is_user=True,
        is_chatbot=False,
        message=audio_user_text,
    )

    session_history = conversation_repository.list_messages_by_session(
        tags.get("session_id")
    )

    process_user_request_service = ProcessUserRequestService(
        audio_user_text, session_history
    )

    answer_to_user = process_user_request_service.process_response()

    audio_response_service = AudioResponseService(answer_to_user)
    polly_audio_url = audio_response_service.audio_response_by_polly()
    storage_service.upload_file(audio_name, polly_audio_url.get("audio_url"))

    conversation_repository.load_data_on_conversation_table(
        session_id=tags.get("session_id"),
        message_id=audio_name,
        is_user=False,
        is_chatbot=True,
        message=answer_to_user,
    )

    return HttpResponse(
        body={"response": "Success to generate audio response!"}
    ).lambdaHttpResponse()
