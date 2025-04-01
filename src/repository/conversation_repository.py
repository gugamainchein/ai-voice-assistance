import os
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr


class ConversationRepository:
    def __init__(self) -> None:
        dynamodb = boto3.resource("dynamodb")
        self._table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE"))

    def load_data_on_conversation_table(
        self,
        session_id: str,
        message_id: str,
        is_user: bool,
        is_chatbot: bool,
        message: str,
    ) -> None:
        message_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._table.put_item(
            Item={
                "session_id": session_id,
                "message_id": message_id,
                "user": is_user,
                "chatbot": is_chatbot,
                "message": message,
                "message_timestamp": message_timestamp,
            }
        )

    def list_messages_by_session(self, session_id: str) -> list[dict]:
        response = self._table.scan(
            FilterExpression=Attr("session_id").eq(session_id),
        )
        return response.get("Items", [])
