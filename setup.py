import os

from setuptools import setup, find_packages

from publicauth import VERSION, PROJECT


BASE_DIR = os.path.abspath(os.path.join( os.path.dirname( __file__ ), 'publicauth', 'templates'))
PACKAGE_DATA = list()

for root, dirs, files in os.walk( BASE_DIR ):
    for filename in files:
        PACKAGE_DATA.append("%s/%s" % ( root[8:], filename ))


setup(
    name = PROJECT,
    version = VERSION,
    description = "django authentication application.",
    long_description = """
        **Download:**
            - git clone http://github.com/klen/django-publicauth.git
    """,
    license = "BSD",

    author = "Kirill Klenov",
    author_email = "horneds@gmail.com",

    url = "http://github.com/klen/django-publicauth.git",

    packages = find_packages(),
    package_data = { '': PACKAGE_DATA, },

    install_requires = [ 'python-openid' ],
)

