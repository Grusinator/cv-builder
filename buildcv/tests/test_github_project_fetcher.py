import os

from cv_content.repositories.github_projects_repository import GitHubProjectsRepository


class TestGithubProjectFetcher:
    def test_fetch_all(self):
        repository = GitHubProjectsRepository(os.getenv("GITHUB_TOKEN"))
        projects = repository._fetch_all()
        assert len(projects) > 0
        cached = repository._fetch_all()
        assert projects == cached
