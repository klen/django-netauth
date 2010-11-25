..   -*- mode: rst -*-

django-netauth
##############

*Django netauth* is django application that allows authenticate users through OpenID/OAuth/Facebook/Vkontakte.

.. contents::

Requirements
-------------

- python >= 2.5
- django >= 1.2
- pip >= 0.8


Installation
------------

*Django netauth* should be installed using pip: ::

    pip install git+git://github.com/klen/django-netauth.git

Setup
------

- Add 'netauth' to INSTALLED_APPS ::

  INSTALLED_APPS += ( netauth, )

- Add 'netauth.middleware.RedirectMiddleware' to MIDDLEWARE_CLASSES ::

  MIDDLEWARE_CLASSES += ( netauth.middleware.RedirectMiddleware, )

