import os

from setuptools import setup, find_packages

from publicauth import VERSION, PROJECT


package_data = list()
for root, dirs, files in os.walk( 'sitegen/templates' ):
    for filename in files:
        package_data.append("%s/%s" % ( root[8:], filename ))


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
    package_data = { '': package_data, },

    install_requires = [ 'python-openid' ],
)

