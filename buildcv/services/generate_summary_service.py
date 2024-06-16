from loguru import logger

from utils.llm_connector import LlmConnector


class GenerateSummaryService:

    def __init__(self):
        self.chatgpt_interface = LlmConnector()

    def generate_summary_from_llm(self, summary_guidance, job_post, job_positions, education, projects, profile_description):
        question = f"""
            Question:
            Write a intro phrase for my cv of how i can contribute to this job. 4 lines of why im a good fit for this job.
            Please dont overexaggerate, just be honest, based on what you know about me, jobs and projects,
            if im not a great fit, just say so, but be constructive, about other things that i can contribute with.
            Feel free to mention the company name and job title.
            please direct it in the focus of:
            
            {summary_guidance}
            ------------------
            Here is the job post. 
            {job_post} 
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
            consider the following profile description: 
            {profile_description}
            make it short. its for a cv intro section. max 4 sentences.
        """.lstrip()
        summary = self.chatgpt_interface.ask_question(question)
        logger.debug(f"Summary: {summary}")
        return summary
