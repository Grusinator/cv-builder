from dotenv import load_dotenv

from dotenv import load_dotenv

from cv_compiler.llm_connector import LlmConnector
from cv_content.schemas import JobPosition, Education

load_dotenv()


class ExtractCvContentFromPdfService:

    def __init__(self):
        self.chatgpt_interface = LlmConnector()


    def get_job_positions_from_pdf(self, cv_text_with_job_positions):
        question = f"""
        Extract job positions from this pdf. it has to be stored in json format, with these fields, 
        please save dates as yyyy-mm-dd, just assume first in month if day is not given.
        {JobPosition.__fields__.keys()}
        Job positions can be found in the following text:
        ------------------
        {cv_text_with_job_positions}
        """
        return self.chatgpt_interface.ask_question_that_returns_pydantic_list(question, JobPosition)

    def get_educations_from_pdf(self, cv_text_with_educations):
        question = f"""
         Extract education from this pdf. it has to be stored in json format, with these fields:
         please save dates as yyyy-mm-dd, just assume first in month if day is not given.
         {Education.__fields__.keys()}
         Education can be found in the following text:
         ------------------
         {cv_text_with_educations}
         """
        return self.chatgpt_interface.ask_question_that_returns_pydantic_list(question, Education)


if __name__ == '__main__':
    cv_content_builder = ExtractCvContentFromPdfService()
