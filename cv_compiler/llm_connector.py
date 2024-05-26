import openai

class ChatGPTInterface:
    def __init__(self, api_key):
        openai.api_key = api_key

    def ask_question(self, question):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )

        answer = response.choices[0].text.strip()
        return answer