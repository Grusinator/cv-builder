import json
import os
import re

from loguru import logger
from openai import OpenAI

from cv_compiler.cache import cache


class LlmConnector:
    def __init__(self):
        self.client = OpenAI(
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID"),
        )
        self.model_name = "gpt-4-turbo"

    def __str__(self):
        return f"ChatGPTInterface(model_name={self.model_name})"

    @cache
    def ask_question(self, question):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": question}],
            max_tokens=3000,
        )
        answer = response.choices[0].message.content
        return answer

    def try_load_as_json_list(self, response):
        try:
            competencies_ordered = json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Invalid response: {response}")
            competencies_ordered = json.loads(re.findall(r'\[.*?\]', response, re.DOTALL)[0])
        assert self.is_list_of_strings(competencies_ordered), ValueError
        return competencies_ordered

    def try_load_as_pydantic_list(self, response, model):
        try:
            json_data = json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Invalid response: {response}")
            json_string = re.findall(r'\[.*\]', response, re.DOTALL)[0]
            json_data = json.loads(json_string)
        response_objects = [model(**comp) for comp in json_data]
        return response_objects

    def ask_question_that_returns_pydantic_list(self, question, model):
        response = self.ask_question(question)
        try:
            return self.try_load_as_pydantic_list(response, model)
        except json.JSONDecodeError as e:
            modified_question = f"""
            {question}
            ----------------
            the above question did not return a valid response, the response was: 
            {response}
            ----------------
            The error was: 
            {e}
            ----------------
            please fix the Json decode error.            
            """
            response = self.ask_question(modified_question)
            return self.try_load_as_pydantic_list(response, model)

    def is_list_of_strings(self, input_list):
        return isinstance(input_list, list) and all(isinstance(elm, str) for elm in input_list)

