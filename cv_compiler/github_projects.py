import os
from datetime import datetime

import requests
from typing import Dict, List
from dotenv import load_dotenv

from cv_compiler.cache import cache
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

    def fetch_topics(self, owner: str, repo: str) -> List[str]:
        url = f'https://api.github.com/repos/{owner}/{repo}/topics'
        self.headers['Accept'] = 'application/vnd.github.mercy-preview+json'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return list(response.json()["names"])

    def fetch_all(self) -> List[GithubProject]:
        repos = self.fetch_all_repos()
        projects = []
        for repo in repos:
            owner = repo['owner']['login']
            repo_name = repo['name']
            topics = self.fetch_topics(owner, repo_name)
            commit_activity = self.fetch_commit_activity(owner, repo_name)
            languages = self.fetch_languages(owner, repo_name)
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
            projects.append(project)
        return projects


if __name__ == "__main__":
    load_dotenv()
    fetcher = GitHubProjectFetcher()
    fetcher.fetch_all()
