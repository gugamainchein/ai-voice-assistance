import json


class HttpResponse:
    def __init__(
        self,
        body: dict,
        statusCode: int = 200,
        content_type: str = "application/json",
        is_base_64: bool = False,
        is_audio: bool = False,
    ) -> None:
        self.body = body
        self.statusCode = statusCode
        self.content_type = content_type
        self.is_base_64 = is_base_64
        self.is_audio = is_audio

    def lambdaHttpResponse(self) -> dict:
        body = self.body
        if self.content_type == "application/json":
            body = json.dumps(self.body)

        response = {
            "statusCode": self.statusCode,
            "headers": {
                "Content-Type": self.content_type,
                "Access-Control-Allow-Origin": "*",
            },
            "body": body,
            "isBase64Encoded": self.is_base_64,
        }

        if self.is_audio:
            response["headers"][
                "Content-Disposition"
            ] = "attachment; filename=response.mp3"

        return response
