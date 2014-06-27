__author__ = 'ggentile'

import unittest
from FrenchLawModel import Text, Article, Version, Law


class test_Text(unittest.TestCase):
    def setUp(self):
        law1 = Law()
        law1.number = 1
        law2 = Law()
        law2.number = 2

        self.text = Text()
        article1 = Article()
        version1 = Version()

        version2 = Version()
        version2.law = law1
        article1.add_version(version1)
        article1.add_version(version2)

        article2 = Article()
        version3 = Version()
        version4 = Version()
        version4.law = law1
        version5 = Version()
        version5.law = law2
        article2.add_version(version3)
        article2.add_version(version4)
        article2.add_version(version5)

    def tearDown(self):
        pass

    def test_get_laws_by_number(self):
        laws = self.text.get_laws_by_number()
        self.assertEqual(len(laws), 3)
        self.assertIsNone(laws[0])
        self.assertEqual(Laws[1], 1)
        self.assertEqual(Laws[2], 2)
        
