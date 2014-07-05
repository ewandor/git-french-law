from config import GIT_REPO_PATH
from git.repo import Repo



class GitLawClient(object):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def get_file_path(self, article):
        return self.repo_path + '/' + article.title

    def commit_law(self, law):
        index = self.repo.index

        modified_files = []
        for article in law.modified_text_article_version:
            file_path = self.get_file_path(article)
            f = open(file_path, 'w')
            f.write(article.body)
            f.close()
            modified_files.append(file_path)
        index.add(modified_files)

        removed_files = []
        for article in law.abrogated_text_article_version:
            file_path = self.get_file_path(article)
            removed_files.append(file_path)
        index.remove(removed_files)

        new_commit = index.commit(law.title)
        #new_commit.committed_date(law.date)



