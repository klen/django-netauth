import os

from setuptools import setup, find_packages

from publicauth import VERSION, PROJECT


MODULE_NAME = 'publicauth'
PACKAGE_DATA = list()

for root, dirs, files in os.walk( os.path.join( MODULE_NAME, 'templates' )):
    for filename in files:
        PACKAGE_DATA.append("%s/%s" % ( root[len(MODULE_NAME)+1:], filename ))


META_DATA = dict(
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

    install_requires = [ 'python-openid', 'oauth2' ],
)


if __name__ == "__main__":
    setup( **META_DATA )

