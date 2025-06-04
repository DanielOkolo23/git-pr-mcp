import unittest
from src.git_pr_mcp.server import _parse_repo_url

class TestParseRepoURL(unittest.TestCase):

    def test_https_with_git_suffix(self):
        url = "https://github.com/testowner/testrepo.git"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "testowner")
        self.assertEqual(name, "testrepo")

    def test_https_without_git_suffix(self):
        url = "https://github.com/anotherowner/anotherrepo"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "anotherowner")
        self.assertEqual(name, "anotherrepo")

    def test_ssh_format(self):
        url = "git@github.com:sshowner/sshrepo.git"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "sshowner")
        self.assertEqual(name, "sshrepo")

    def test_ssh_format_without_git_suffix(self):
        # The regex should also handle this if the .git is optional at the end
        url = "git@github.com:owner/repo"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "owner")
        self.assertEqual(name, "repo")

    def test_url_with_hyphens_and_numbers(self):
        url = "https://github.com/owner-123/repo-name-456.git"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "owner-123")
        self.assertEqual(name, "repo-name-456")
        
        url_no_suffix = "https://github.com/owner-123/repo-name-456"
        owner_no_suffix, name_no_suffix = _parse_repo_url(url_no_suffix)
        self.assertEqual(owner_no_suffix, "owner-123")
        self.assertEqual(name_no_suffix, "repo-name-456")

    def test_specific_user_url(self):
        url = "https://github.com/peterj/mcpplayground.git"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "peterj")
        self.assertEqual(name, "mcpplayground")

    def test_gitlab_url(self):
        # The current regex is specific to github.com if domain matching is strict,
        # but it uses [^/]+ which should allow other domains.
        # Let's test assuming it's somewhat generic for the structure.
        url = "https://gitlab.com/gitlabowner/gitlabrepo.git"
        owner, name = _parse_repo_url(url)
        # Based on the regex `(?:https?://[^/]+/|git@[\w\.-]+:)` the domain part is generic.
        self.assertEqual(owner, "gitlabowner")
        self.assertEqual(name, "gitlabrepo")

    def test_invalid_urls(self):
        invalid_urls = [
            "https://github.com/owneronly", # Not enough parts
            "ftp://github.com/owner/repo.git", # Wrong protocol for the git@ part of regex
            "JustARandomString",
            "https/github.com/owner/repo.git",
            "https://github.com/",
            "git@github.com",
            "git@github.com:",
            "git@github.com:/",
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                owner, name = _parse_repo_url(url)
                self.assertIsNone(owner, f"Owner should be None for {url}")
                self.assertIsNone(name, f"Name should be None for {url}")
    
    def test_url_with_dot_in_repo_name(self):
        # The regex `([^/\\.]+?)` for repo name might have issues with dots
        # The pattern is `([^/\\.]+?)` which means "one or more characters that are not a slash or a dot, non-greedy".
        # This implies it will stop at the first dot. This test will likely fail with the current regex if the repo name has dots.
        # Example: if repo is "my.repo.project" it would parse as "my"
        # Let's confirm this behavior.
        url = "https://github.com/testowner/my.repo.name.git"
        owner, name = _parse_repo_url(url)
        self.assertEqual(owner, "testowner")
        # Based on regex `([^/\\.]+?)`, it should capture "my"
        # If the intention is to capture "my.repo.name", the regex needs adjustment for the name part.
        # Current regex: ([^/\\.]+?)
        # To capture dots in repo name, it could be: ([^/]+?) but then .git needs careful handling.
        # Or, more simply, if .git is always the suffix to be removed: ([^/]+?) then remove .git if present.
        # The current regex is `([^/\\.]+?)(?:\\.git)?$`.
        # This means `name` is "one or more chars NOT / or ." followed by an optional ".git".
        # So "my.repo.name.git" -> name will be "my"
        # "myrepo.git" -> name will be "myrepo"
        # "my.repo" (no .git suffix) -> name will be "my"
        self.assertEqual(name, "my.repo.name")

        url_no_suffix = "https://github.com/testowner/my.repo"
        owner_no_suffix, name_no_suffix = _parse_repo_url(url_no_suffix)
        self.assertEqual(owner_no_suffix, "testowner")
        self.assertEqual(name_no_suffix, "my.repo")


if __name__ == '__main__':
    unittest.main() 