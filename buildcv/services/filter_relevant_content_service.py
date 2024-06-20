import json
from typing import List

import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from buildcv.models import JobPost
from cv_content.repositories import CvContentRepository
from cv_content.schemas import Competency, Project
from cv_content.schemas import GithubProject
from utils.llm_connector import LlmConnector


class SimilarityByVector:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def find_most_relevant_indices(self, job_description: str, items: List[str]) -> List[int]:
        # Embed the job description and items
        job_desc_embedding = self.model.encode([job_description])
        item_embeddings = self.model.encode(items)
        similarities = cosine_similarity(job_desc_embedding, item_embeddings)[0]

        sorted_indices = np.argsort(similarities)[::-1]

        return sorted_indices.tolist()


class FilterRelevantContentService:

    def __init__(self):
        self.llm_connector = LlmConnector()
        self.similarity_by_vector = SimilarityByVector()
        self.cv_content_repository = CvContentRepository()

    def find_most_relevant_competencies(self, job_post: JobPost, n=10) -> List[
        Competency]:
        competencies = self.cv_content_repository.get_competencies(job_post.user)
        sorted_competencies = self.sort_competencies_by_similarity(job_post, competencies)

        if len(sorted_competencies) > n:
            sorted_competencies = sorted_competencies[:n]

        logger.debug(f"Most attractive competencies: {sorted_competencies}")
        return sorted_competencies

    def sort_competencies_by_similarity(self, job_post, competencies):
        competency_names = [f"We are looking for experience in {comp.name}" for comp in competencies]
        relevant_indices = self.similarity_by_vector.find_most_relevant_indices(job_post.job_post_text,
                                                                                competency_names)
        sorted_competencies = [competencies[i] for i in relevant_indices]
        return sorted_competencies

    def find_most_relevant_projects(self, job_post: JobPost, n=10) -> List[Project]:
        user = job_post.user
        projects = self.cv_content_repository.get_projects(user)
        sorted_projects = self.sort_projects_by_similarity(job_post, projects)

        if len(sorted_projects) > n:
            sorted_projects = sorted_projects[:n]
        logger.debug(f"Most relevant projects: {sorted_projects}")
        return sorted_projects

    def sort_projects_by_similarity(self, job_post, projects):
        project_descriptions = [f"{proj.name} {proj.description} {' '.join(proj.competencies)}" for proj in projects]
        relevant_indices = self.similarity_by_vector.find_most_relevant_indices(job_post.job_post_text,
                                                                                project_descriptions)
        sorted_projects = [projects[i] for i in relevant_indices]
        return sorted_projects

    def filter_most_relevant_projects(self, projects: List[GithubProject], competencies: List[Competency]):
        known_languages = {comp.name for comp in competencies}
        filtered_projects = [
            proj for proj in projects if
            len(set(proj.languages + proj.topics).intersection(known_languages)) > 0
        ]
        projects = sorted(filtered_projects, key=lambda x: x.commits, reverse=True)
        return projects

    def find_most_relevant_competencies_to_job_add(self, job_description: str, competencies: List[Competency], n=10) -> \
            List[
                Competency]:
        competencies_ordered = self._filter_matching_competencies_from_job_application(competencies, job_description)

        if len(competencies_ordered) > n:
            competencies_ordered = competencies_ordered[:n]
        attractive_competencies = [comp for comp in competencies if comp.name in competencies_ordered]
        logger.debug(f"Most attractive competencies: {attractive_competencies}")
        return attractive_competencies

    def _filter_matching_competencies_from_job_application(self, competencies: List[Competency],
                                                           job_description: str) -> List[str]:
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
