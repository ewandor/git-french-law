from pyquery import PyQuery as Q
from urllib import urlencode
from urlparse import parse_qs
from datetime import datetime

class LegiFrancePage(object):
    adress = ''

    def set_content(self, content):
        self.content = content
        self.dom = Q(content)
        self.data = Q(self.dom('.data'))

    def set_articles(self, articles_data):
        for article_html in self.data('.article'):
            article_dom = Q(article_html)
            articles_data.append(
                {'title': article_dom('.titreArt'), 'body': [paragraph.text for paragraph in article_dom('p')]})
            article_id_list.append(article_dom('.histoArt .liensArtResolu'))


class TextPage(LegiFrancePage):
    action = 'affichTexte.do'
    cidText = ''

    def get_adress(self):
        return self.action + '?' + urlencode({'cidTexte': self.cidText})


class ConstitutionPage(TextPage):
    cidText = 'LEGITEXT000006071194'

    def get_article_list(self):
        article_list = []
        for link in self.dom('.titreArt a'):
            query = Q(link).attr('href').split('?')[1]
            article_list.append(parse_qs(query)['idArticle'][0])
        return article_list


class ArticlePage(LegiFrancePage):
    def __init__(self, text_page, article_id, date=None):
        self.text_page = text_page
        self.idArticle = article_id
        self.dateTexte = date

    def get_adress(self):
        if self.dateTexte is None:
            return 'affichTexteArticle.do?' + urlencode(
                {'cidTexte': self.text_page.cidText, 'idArticle': self.idArticle}
                )
        else:
            return 'affichTexteArticle.do?' + urlencode(
                {'cidTexte': self.text_page.cidText, 'idArticle': self.idArticle, 'dateTexte': self.dateTexte}
                )

    def set_article_version(self, version):
        if self.dateTexte is None:
            raise Exception()

        version.title = self.dom('.titreArt').text()
        version.body = self.dom('.corpsArt').text()
        version.histo = self.dom('.histoArt').text()

    def get_article_version_list(self):
        version_list = []
        for link in self.dom('#left_menu .pGauche:eq(1) a'):
            query = Q(link).attr('href').split('?')[1]
            version_list.append(parse_qs(query)['dateTexte'][0].strip())
        return version_list

class LawPage(ArticlePage):
    REGEX_TITLE = r'n°(?P<number>[\d-]+) du (?P<date>\d+ \S+ \d{4})'

    def set_law(self, law):
        law.title = self.dom('.data a strong').text()
        res = re.search(REGEX_TITLE, law.title)
        law.number = res.group('number')
        law.date = self.parse_date(res.group('date'))

    @staticmethod
    def parse_date(date_string):
        import locale
        locale.setlocale(locale.LC_ALL, ('fr', 'utf-8'))
        return datetime.strptime(date, '%d %B %Y')

