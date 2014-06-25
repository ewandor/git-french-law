from git.errors import NoSuchPathError
import os

import shutil

import GitLawClient
__author__ = 'ggentile'

import unittest

from git.repo import is_git_dir

class test_GitLawClient(unittest.TestCase):
    def setUp(self):
        self.test_dir = '/tmp/test_gitlawclient'
        os.mkdir(self.test_dir)

    def tearDown(self)
        shutil.rmtree('/tmp/test_gitlawclient')

    def test_create_non_existing_directory(self):
        self.assertRaises(NoSuchPathError, GitLawClient.__init__, self.test_dir + '/non/existing/path')

    def test_create_non_git_non_empty_directory(self):
        dir = self.test_dir + '/non_git_non_empty_directory'
        os.mkdir(dir)
        f = open(dir + '/empty_file', 'a')
        f.write('this is an empty file to test non git non empty directory')
        f.close
        self.assertRaises(NonEmptyDirectory, GitLawClient.__init__, dir)

    def test_create_existing_non_git_directory(self):
        dir = self.test_dir + '/non_git_directory'
        os.mkdir(dir)
        GitLawClient.__init__(dir)
        self.assertTrue(is_git_dir(dir))

    def test_create_with_matching_git_directory(self):
        pass

    def test_create_with_non_matching_git_directory(self):

