# -*- coding: utf-8 -*-

from pyquery import PyQuery as Q
import re
from urllib import urlencode
from urlparse import parse_qs
from datetime import datetime

from FrenchLawModel import version_historic

version_historic_mapping = {
    u'Créé par': version_historic.created_by,
    u'Modifié par': version_historic.modified_by,
    u'Abrogé par': version_historic.abrogated_by,
}

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
            article_list.append(''.join(parse_qs(query)['idArticle'][0].split()))
        return article_list


class ArticlePage(LegiFrancePage):
    REGEX_HISTORIC = ur'(?P<status>\S+ par)'

    def __init__(self, text_page, article_id, date=None):
        self.text_page = text_page
        self.idArticle = article_id
        self.dateTexte = date
        self.abrogating_law_page = None
        self.modifying_law_page = None

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

        for entry in self.dom('.histoArt li'):
            entry_dom = Q(entry)
            url_to_law = entry_dom('a').attr('href')
            query = parse_qs(url_to_law.split('?')[1])
            if 'idArticle' in query:
                law_page = LawPage(query['cidTexte'][0], query['idArticle'][0])
                res = re.search(self.REGEX_HISTORIC, entry_dom.text())
                if version_historic_mapping[res.group('status')] == version_historic.abrogated_by:
                    self.abrogating_law_page = law_page
                elif version_historic_mapping[res.group('status')] in\
                        [version_historic.created_by, version_historic.modified_by]:
                    self.modifying_law_page = law_page


    def get_article_version_list(self):
        version_list = []
        for link in self.dom('#left_menu .pGauche:eq(1) a'):
            query = Q(link).attr('href').split('?')[1]
            version_list.append(parse_qs(query)['dateTexte'][0].strip())
        return version_list

class LawPage(ArticlePage):
    REGEX_TITLE = ur'n°\s?(?P<number>[\d-]+) du (?P<date>\d+ \S+ \d{4})'
    existing_laws = {}

    def __init__(self, cid_text, article_id):
        self.cidTexte = cid_text
        self.idArticle = article_id

    def get_adress(self):
        return 'affichTexteArticle.do?' + urlencode(
            {'cidTexte': self.cidTexte, 'idArticle': self.idArticle}
        )

    def set_law(self, law):
        title = self.dom('.data a strong').text()
        res = re.search(self.REGEX_TITLE, title)
        number = res.group('number')
        if number in self.existing_laws:
            law = self.existing_laws[number]
        else:
            law.title = title
            law.number = number
            law.date = self.parse_date(res.group('date'))
            self.existing_laws[number] = law

        return law

    @staticmethod
    def parse_date(date_string):
        import locale
        locale.setlocale(locale.LC_ALL, ('fr', 'utf-8'))
        return datetime.strptime(date_string.encode("utf-8"), '%d %B %Y')

