import os

import pytest
from openai import OpenAIError

from utils.llm_connector import LlmConnector


def test_llm_connector_fails_if_no_env_vars():
    del os.environ["OPENAI_PROJECT_ID"]
    del os.environ["OPENAI_ORG_ID"]
    del os.environ["OPENAI_API_KEY"]
    llm = LlmConnector()
    with pytest.raises(OpenAIError):
        llm.ask_question("What is your name?")
