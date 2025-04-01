class HttpRequest:
    def __init__(
        self,
        body: dict = None,
        queryStringParameters: dict = None,
        Records: list = None,
        path: dict = None,
    ) -> None:
        self.body = body
        self.queryStringParameters = queryStringParameters
        self.Records = Records
        self.path = path
