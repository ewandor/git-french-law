from enum import Enum

version_status = Enum('in_effect', 'modified', 'abrogated')
version_historic = Enum('created_by', 'modified_by', 'abrogated_by')

class Text(object):
    def __init__(self):
        self.articles = []
        self.modifying_laws = []

    def add_article(self, article):
        article.text = self
        self.articles.append(article)
        for version in article.versions:
            if not version.modifying_law is None:
                if not version.modifying_law in self.modifying_laws:
                    self.modifying_laws.append(version.modifying_law)
            if not version.abrogating_law is None:
                if not version.abrogating_law in self.modifying_laws:
                    self.modifying_laws.append(version.abrogating_law)

    def get_laws_by_date(self):
        return sorted(self.modifying_laws, key=lambda law: law.date)

class Article(object):
    def __init__(self):
        self.versions = []

    def add_version(self, version):
        version.article = self
        self.versions.append(version)

    def get_status(self):
        return self.versions[-1].status

class Law(object):
    def __init__(self):
        self.title = None
        self.number = None
        self.date = None
        self.modified_text_article_version = []
        self.abrogated_text_article_version = []

    def __repr__(self):
        return self.title.encode("ascii", 'ignore')

class Version(object):
    def __init__(self):
        self.modifying_law = None
        self.abrogating_law = None

    def set_modifying_law(self, law):
        law.modified_text_article_version.append(self)
        self.modifying_law = law

    def set_abrogating_law(self, law):
        law.abrogated_text_article_version.append(self)
        self.abrogating_law = law
