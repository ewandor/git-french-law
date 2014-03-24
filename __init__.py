from mechanize import Browser
from pyquery import PyQuery as Q

class LegifranceClient(object):

    host = 'http://www.legifrance.gouv.fr/'

    def __init__(self):
        self.browser = Browser()

    def get_page(self, page):
        self.browser.open(self.host + page.adress)
        return page(self.browser.response().read())

    def get_constitution(self):
        articles = {}
        return self.get_page(ConstitutionPage)

class Page(object):

    adress = ''

    def __init__(self, content):
        self.content = content
        self.dom = Q(content)

    def set_articles(self, articles):
        pass


class ConstitutionPage(Page):

    adress = 'affichTexte.do?cidTexte=LEGITEXT000006071194'

class Article(object):
    pass

cli = LegifranceClient()
print cli.get_constitution().dom('#subcontent')