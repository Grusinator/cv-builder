import os
from datetime import datetime

THIS_MONTH = datetime.now().strftime("%Y %m")

import requests
from typing import Dict, List
from dotenv import load_dotenv
from loguru import logger

from utils.cache import cache
from cv_content.schemas import GithubProject


class GitHubProjectsRepository:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError('GitHub token is required')
        self.headers = {'Authorization': f'token {self.token}'}
        self._projects = []

    def get_projects(self):
        if len(self._projects) == 0:
            self._projects = self._fetch_all()
        return self._projects

    def _fetch_all(self) -> List[GithubProject]:
        logger.debug(f'Fetching all projects from GitHub')
        repos = self._fetch_all_repos()
        projects = []
        for repo in repos:
            owner = repo['owner']['login']
            repo_name = repo['name']
            topics = self._fetch_topics(owner, repo_name)
            commit_activity = self._fetch_commit_activity(owner, repo_name)
            languages = self._fetch_languages(owner, repo_name)
            project = GithubProject(
                name=repo_name,
                owner=owner,
                commits=sum(commit_activity['all']),
                description=repo['description'],
                number_of_weeks_with_commits=len([week for week in commit_activity['all'] if week > 0]),
                topics=topics,
                last_commit=datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
                languages=list(languages.keys()),  # Update this line
                technologies=[]  # Fill this with actual data
            )
            logger.debug(f'Fetched project: {project}')
            projects.append(project)
        return projects

    @cache
    def _fetch_all_repos(self, fetch_date_for_caching=THIS_MONTH) -> List[Dict]:
        url = 'https://api.github.com/user/repos'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @cache
    def _fetch_topics(self, owner: str, repo: str, fetch_date_for_caching=THIS_MONTH) -> List[str]:
        url = f'https://api.github.com/repos/{owner}/{repo}/topics'
        self.headers['Accept'] = 'application/vnd.github.mercy-preview+json'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return list(response.json()["names"])

    @cache
    def _fetch_commit_activity(self, owner: str, repo: str, fetch_date_for_caching=THIS_MONTH) -> Dict:
        url = f'https://api.github.com/repos/{owner}/{repo}/stats/participation'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @cache
    def _fetch_languages(self, owner: str, repo: str, fetch_date_for_caching=THIS_MONTH) -> Dict[str, int]:
        url = f'https://api.github.com/repos/{owner}/{repo}/languages'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    load_dotenv()
    fetcher = GitHubProjectsRepository()
    fetcher._fetch_all()
