import os

from openai import OpenAI


class ChatGPTInterface:
    def __init__(self):
        self.client = OpenAI(
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID"),
        )

    def ask_question(self, question):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=500,
        )
        answer = response.choices[0].message.content
        return answer
