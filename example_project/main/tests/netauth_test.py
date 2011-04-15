from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from netauth import settings


class NetauthTestCase( TestCase ):

    def setUp( self ):
        self.client = Client()

    def test_login(self):
        url = reverse("netauth-login")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_google(self):
        url = reverse("netauth-begin", args=["google"])
        response = self.client.get(url, data={"openid_url":"https://www.google.com/accounts/o8/id"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith("https://www.google.com/accounts/o8/ud"))

    def test_twitter(self):
        url = reverse("netauth-begin", args=["twitter"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith(settings.TWITTER_AUTHORIZE_URL))
