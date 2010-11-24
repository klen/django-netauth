from django.db import models
from django.contrib.auth.models import User


class PublicID(models.Model):
    user = models.ForeignKey(User)
    identity = models.CharField(u'Public ID', max_length=255, unique=True)
    provider = models.CharField(u'Public authentication provider name', max_length=255)

    def __unicode__(self):
        return "%s -> %s" % (self.provider, self.identity)
