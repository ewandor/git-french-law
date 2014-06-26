from enum import Enum

version_status = Enum('in_effect', 'modificated', 'abrogated')

class Text(object):
    def __init__(self):
        self.articles = []

    def append(self, article):
        self.articles.append(article)

    def get_laws(self):
        laws = []
        for article in self.articles:
            laws.append(article.version.law)

class Article(object):
    def __init__(self):
        self.versions = []

    def add_version(self, version):
        self.versions.append(version)

    def get_status(self):
        return self.versions[-1].status

class Law(object):
    pass

class Version(object):
    pass