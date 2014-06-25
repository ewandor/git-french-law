from config import GIT_REPO_PATH
from git.repo import Repo



class GitLawClient(object):
    def __init__(repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def commit_law(self, law):
        index = self.repo.index

        for article in law.articles:
            index.add(article)
            new_commit = index.commit(law.title)
            #new_commit.committed_date(law.date)



