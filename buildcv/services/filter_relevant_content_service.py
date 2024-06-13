from typing import List

from cv_content.schemas import GithubProject, Competency
from utils.llm_connector import LlmConnector

class FilterRelevantContentService:

    def __init__(self):
        self.llm_connector = LlmConnector()
    def filter_most_relevant_projects(self, projects: List[GithubProject], competencies: List[Competency]):
        known_languages = {comp.name for comp in competencies}
        filtered_projects = [
            proj for proj in projects if
            len(set(proj.languages + proj.topics).intersection(known_languages)) > 0
        ]
        projects = sorted(filtered_projects, key=lambda x: x.commits, reverse=True)
        return projects

    def filter_matching_competencies_from_job_application(self, competencies: List[Competency], job_description):
        competency_names = [comp.name for comp in competencies]
        question = f"""
        sort these competencies by attractiveness for this job, focus on the title and tell me what skills 
        are relevant for this job. also look at the skills mentioned in the job description, 
        and if there are similar skill, then put them in the top. 

        Job decription:
        {job_description}
        --------------------
        Competencies:        
        {json.dumps(competency_names)}
        --------------------
        it should be formattet as json as a list of strings, and the response should only include the json list, like this:

        ["Python", "Data engineering", "Machine learning"]

        """
        response = self.llm_connector.ask_question(question)
        logger.debug(f"Response: {response}")
        competencies_matching = self.llm_connector.try_load_as_json_list(response)
        return competencies_matching
