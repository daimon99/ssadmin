# coding:utf-8

from django.test.testcases import SimpleTestCase


class SSTestCase(SimpleTestCase):
    allow_database_queries = True

    def test_show_port(self):
        from ssadmin.services import show_port
        ret = show_port(10000)
        print ret
