import os
from datetime import datetime

import requests
from typing import Dict, List

from cv_compiler.models import GithubProject


class GitHubProjectFetcher:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError('GitHub token is required')
        self.headers = {'Authorization': f'token {self.token}'}

    def fetch_all_repos(self) -> List[Dict]:
        url = 'https://api.github.com/user/repos'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_commit_activity(self, owner: str, repo: str) -> Dict:
        url = f'https://api.github.com/repos/{owner}/{repo}/stats/participation'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_languages(self, owner: str, repo: str) -> Dict[str, int]:
        url = f'https://api.github.com/repos/{owner}/{repo}/languages'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_all(self) -> List[GithubProject]:
        repos = self.fetch_all_repos()
        projects = []
        for repo in repos:
            commit_activity = self.fetch_commit_activity(repo['owner']['login'], repo['name'])
            languages = self.fetch_languages(repo['owner']['login'], repo['name'])
            project = GithubProject(
                name=repo['name'],
                owner=repo['owner']['login'],
                commits=sum(commit_activity['all']),
                number_of_weeks_with_commits=len([week for week in commit_activity['all'] if week > 0]),
                last_commit=datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
                languages=list(languages.keys()),  # Update this line
                technologies=[]  # Fill this with actual data
            )
            projects.append(project)
        return projects


if __name__ == "__main__":
    fetcher = GitHubProjectFetcher()
    fetcher.fetch_all()
