import pytest
from mock.mock import MagicMock

from cv_compiler.llm_connector import ChatGPTInterface


@pytest.fixture
def mock_llm():
    llm = ChatGPTInterface()
    llm.ask_question = MagicMock(return_value="mocked response")
    llm.try_load_as_json_list = MagicMock(return_value=['python', 'Java'])
    return llm
