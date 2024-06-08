from loguru import logger

from utils.llm_connector import LlmConnector


class GenerateSummaryService:

    def __init__(self):
        self.chatgpt_interface = LlmConnector()

    def generate_summary_from_llm(self, job_desc, job_positions, education, projects):
        question = f"""
          Write a intro phrase for my cv of how i can contribute to this job. 4 lines of why im a good fit for this job.
          Please dont overexaggerate, just be honest, based on what you know about me, jobs and projects,
          if im not a great fit, just say so, but be constructive, about other things that i can contribute with.
          Feel free to mention the company name and job title. 
          Here is the job post description. 
           {job_desc} 
          ------------------
          consider the following job positions:
          {job_positions}
          ------------------
          consider the following education:
          {education}
          ------------------
          consider the following projects:
          {projects}
          ------------------
          make it short. its for a cv intro section. max 4 sentences.
          """
        summary = self.chatgpt_interface.ask_question(question)
        logger.debug(f"Summary: {summary}")
        return summary
