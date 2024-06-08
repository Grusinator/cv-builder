from cv_content.repositories.github_projects_repository import GitHubProjectsRepository


class TestGithubProjectFetcher:
    def test_fetch_all(self):
        projects = GitHubProjectsRepository()._fetch_all()
        assert len(projects) > 0
        cached = GitHubProjectsRepository()._fetch_all()
        assert projects == cached
