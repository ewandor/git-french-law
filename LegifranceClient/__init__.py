from datetime import datetime
from mechanize import Browser

from FrenchLawModel import Text, Article, Version, Law

from page import ConstitutionPage, ArticlePage


class LegifranceClient(object):
    host = 'http://www.legifrance.gouv.fr/'

    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)'
        self.__init_browser()
        self.create_initial_law()

    def __init_browser(self):
        self.browser = Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [('User-agent', self.user_agent)]

    def get_page(self, page):
        self.browser.open(self.host + page.get_adress())
        page.set_content(self.browser.response().read())
        return page

    def create_initial_law(self):
        self.initial_law = Law()
        self.initial_law.title = "La Constitution du 4 octobre 1958"
        self.initial_law.number = "-1"
        self.initial_law.date = datetime(1958, 10, 4)

    def get_constitution(self):
        constitution = Text()
        page = self.get_page(ConstitutionPage())
        article_list = page.get_article_list()

        for article_id in article_list:
            article = Article()
            page = self.get_page(ArticlePage(ConstitutionPage, article_id))
            article_version_list = page.get_article_version_list()
            for version_id in article_version_list:
                page = self.get_page(ArticlePage(ConstitutionPage, article_id, version_id))
                version = Version()
                page.set_article_version(version)
                if not page.abrogating_law_page is None:
                    law_page = self.get_page(page.abrogating_law_page)
                    law = law_page.set_law(Law())
                    version.set_abrogating_law(law)
                if not page.modifying_law_page is None:
                    law_page = self.get_page(page.modifying_law_page)
                    law = law_page.set_law(Law())
                    version.set_modifying_law(law)
                else:
                    version.set_modifying_law(self.initial_law)

                article.add_version(version)

            constitution.add_article(article)
        return constitution