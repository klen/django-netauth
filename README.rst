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

    pip install django-netauth


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


- See services setup bellow.


Use netauth
------------

1) Use url '/auth/login' as login point in your site
2) Use template tag 'netauth_widget'
3) Create custom interface


Extra fields
-------------
In order to fill extra fields that may be required by your user profile, you need to setup couple of variables in settings.py of your project.

The name of variable should be uppercased name of backend + "_PROFILE_MAPPING". For example: GOOGLE_PROFILE_MAPPING, TWITTER_PROFILE_MAPPING, etc..

The value of this variable must be dictionary with name of the field on the provider side and its value must be name of your form field. For example:

TWITTER_PROFILE_MAPPING = { 'screen_name': 'username', }

Here you can see that 'screen_name' is what you asking from twitter, in your EXTRA_FORM you will see the value of this under key 'username'. This is because every authentication method can provide different names for its data and you need to unify it.

Also you can override the EXTRA_FORM itself and set NETAUTH_EXTRA_FORM variable with value as path to your custom form. Dont forget to implement save method in this form.


Facebook
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
