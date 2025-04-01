import os
import json
import boto3


class ProcessUserRequestService:
    def __init__(self, user_input: str) -> None:
        self.user_input = user_input
        self.model_id = os.environ.get("MODEL_ID")
        self.bedrock = boto3.client("bedrock-runtime")

    def process_response(self) -> str:
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"""Your task is to assist [User's Name] in improving their English speaking skills. Follow this structured approach for each session:

                    Daily Conversations:

                    Begin with simple, everyday topics such as greetings, introductions, and small talk.
                    Engage in a 5-10 minute conversation focusing on these subjects.
                    Role-Playing Scenarios:

                    Conduct role-playing exercises such as ordering food at a restaurant, asking for directions, or having a conversation with a customer service representative.
                    Spend 10-15 minutes on each scenario to practice different contexts.
                    Pronunciation Practice:

                    Identify common pronunciation challenges specific to [User's Native Language].
                    Focus on practicing specific sounds and intonations for 10 minutes each day.
                    Listening and Repeating:

                    Play short audio clips from English podcasts or news segments.
                    After each clip, guide [User's Name] to repeat what they heard.
                    Conduct this for 5-10 minutes daily.
                    Feedback:

                    Provide constructive feedback after each session on pronunciation, fluency, and other speaking aspects.
                    Highlight areas of improvement and offer tips for better practice.
                    Start with today's topic: [Specify a topic, e.g., 'Greetings and Introductions'].

                    Ensure that each session is interactive and engaging to keep [User's Name] motivated and progressing.

                    User: {self.user_input}""",
                },
            ],
            "max_tokens": 1000,
            "anthropic_version": "bedrock-2023-05-31",
        }

        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"].strip()
