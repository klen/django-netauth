from setuptools import setup, find_packages
from publicauth import VERSION, PROJECT

setup(
    name = PROJECT,
    version = VERSION,
    packages = find_packages(),
    author = "Kirill Klenov",
    author_email = "horneds@gmail.com",
    description = "django authentication application.",
    long_description = """
        **Download:**

            - git clone http://github.com/klen/django-publicauth.git

    """,
    license = "BSD",
    keywords = "django",
    url = "http://github.com/klen/django-publicauth.git",
    install_requires = [ 'python-openid' ],
)

