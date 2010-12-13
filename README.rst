..   -*- mode: rst -*-

django-netauth
##############

**Django netauth** is django application that allows authenticate users through OpenID/OAuth/Facebook/Vkontakte.

.. contents::

Requirements
-------------

- python >= 2.5
- django >= 1.2
- pip >= 0.8


Installation
------------

**Django netauth** should be installed using pip: ::

    pip install git+git://github.com/klen/django-netauth.git


Setup
------

- Add 'netauth' to INSTALLED_APPS ::

  INSTALLED_APPS += ( 'netauth', )

- Add 'netauth.middleware.RedirectMiddleware' to MIDDLEWARE_CLASSES ::

  MIDDLEWARE_CLASSES += ( 'netauth.middleware.RedirectMiddleware', )

- Add netauth urls to base urls ::

  url('auth/', include( 'netauth.urls')),

- Add netauth backend to AUTHENTICATION_BACKENDS ::

  AUTHENTICATION_BACKENDS += ( 'netauth.auth.NetBackend', )

See services setup: facebook_, `Twitter`_, `Yandex`_, `Vkontakte`_


Use netauth
------------

1) Use url '/auth/login' as login point in your site
2) Use template tag 'netauth_widget'
3) Create custom interface


.. _facebook: Facebook
---------

- Go to http://www.facebook.com/developers/createapp.php and create application

- Set FACEBOOK_APPLICATION_ID and FACEBOOK_APPLICATION_SECRET in your settings file


Twitter
--------

- Go to http://twitter.com/apps/new and create application

- Set TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET and TWITTER_REQUEST_TOKEN_URL in your settings file


Yandex
-------

- Go to http://oauth.yandex.ru/client/new and create application

- Add YANDEX_APPLICATION_ID in your settings file


Vkontakte
----------

- Go to  http://vkontakte.ru/apps.php?act=add&site=1 and create application

- Add VKONTAKTE_APPLICATION_ID and VKONTAKTE_APPLICATION_SECRET in your settings file


Note
-----

You need to setup messages-framework_ as described in django documentation


.. _messages-framework: http://docs.djangoproject.com/en/dev/ref/contrib/messages/#ref-contrib-messages
