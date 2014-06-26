from mechanize import Browser

from FrenchLawModel import Text, Article, Version, Law

from page import ConstitutionPage, ArticlePage


class LegifranceClient(object):
    host = 'http://www.legifrance.gouv.fr/'

    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)'
        self.__init_browser()

    def __init_browser(self):
        self.browser = Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [('User-agent', self.user_agent)]

    def get_page(self, page):
        self.browser.open(self.host + page.get_adress())
        page.set_content(self.browser.response().read())
        return page

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
                article.add_version(version)
                if not version.histo is None:
                    law_page = self.get_page(page.get_associated_law_page())
                    version.law = Law()
                    law_page.set_law(version.law)
                else:
                    version.law = None

            constitution.append(article)
            break
        return constitution