import json
import os
import re

from loguru import logger
from openai import OpenAI, OpenAIError

from utils.cache import cache
from typing import List
from pydantic import BaseModel


class LlmConnector:
    def __init__(self):
        try:
            self.client = OpenAI(
                organization=os.getenv("OPENAI_ORG_ID"),
                project=os.getenv("OPENAI_PROJECT_ID"),
            )
        except OpenAIError:
            logger.exception("OpenAIError: OpenAI client has not been enabled due to missing accesss tokens")
            self.ask_question = self.raise_access_exception
        self.model_name = "gpt-4-turbo"

    def __str__(self):
        return f"ChatGPTInterface(model_name={self.model_name})"

    def raise_access_exception(self, question):
        raise OpenAIError("OpenAIError: OpenAI client has not been enabled due to missing accesss tokens")

    @cache
    def ask_question(self, question: str):
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
            instances = self.try_load_as_pydantic_list(response, model)
            self.remove_primary_keys(instances)
            return instances

    def is_list_of_strings(self, input_list):
        return isinstance(input_list, list) and all(isinstance(elm, str) for elm in input_list)

    def remove_primary_keys(self, instances: List[BaseModel]):
        for instance in instances:
            primary_keys = [key for key, value in instance.__fields__.items() if
                            value.field_info.extra.get('primary_key')]
            instance[primary_keys[0]] = None
