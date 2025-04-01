import os
from src.helpers.lambda_payload import HttpRequest
from src.helpers.lambda_response import HttpResponse


def handler(event: HttpRequest, context: None) -> HttpResponse:
    try:
        base_dir = os.path.join(os.path.dirname(__file__), "static")
        path = event.get("path", "").replace("/frontend", "").lstrip("/")

        if not path:
            path = "index.html"

        file_path = os.path.join(base_dir, path)
        file_path = file_path.replace("src/controllers/frontend/", "")

        if not os.path.exists(file_path):
            return {"statusCode": 404, "body": "File not found"}

        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
        }

        _, file_extension = os.path.splitext(file_path)
        content_type = content_types.get(
            file_extension.lower(), "application/octet-stream"
        )

        with open(file_path, "rb") as file:
            content = file.read()

        is_binary = content_type.startswith(("image/", "application/"))
        if is_binary:
            import base64

            body = base64.b64encode(content).decode("utf-8")
        else:
            body = content.decode("utf-8")

        return HttpResponse(
            body=body,
            statusCode=200,
            content_type=content_type,
            is_base_64=is_binary,
        ).lambdaHttpResponse()
    except Exception as err:
        return HttpResponse(
            body={"response": {"error": str(err)}}, statusCode=500
        ).lambdaHttpResponse()
