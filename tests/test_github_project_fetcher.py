from cv_compiler.github_project_fetcher import GitHubProjectFetcher


class TestGithubProjectFetcher:
    def test_fetch_all(self):
        projects = GitHubProjectFetcher().fetch_all()
        assert len(projects) > 0
        cached = GitHubProjectFetcher().fetch_all()
        assert projects == cached
