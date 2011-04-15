from django.test import Client, TestCase


class BaseTestCase(TestCase):

    def setUp( self ):
        self.client = Client()

    def test_index(self):
        response = self.client.get('')
        self.assertContains(response, 'login')
