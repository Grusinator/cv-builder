from typing import List

from cv_content.schemas import GithubProject, Competency


class FilterRelevantContentService:
    def filter_most_relevant_projects(self, projects: List[GithubProject], competencies: List[Competency]):
        known_languages = {comp.name for comp in competencies}
        filtered_projects = [
            proj for proj in projects if
            len(set(proj.languages + proj.topics).intersection(known_languages)) > 0
        ]
        projects = sorted(filtered_projects, key=lambda x: x.commits, reverse=True)
        return projects
