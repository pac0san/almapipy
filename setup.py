# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

from almapipy.__init__ import __version__ as version
from almapipy.__init__ import __author__ as author
from almapipy.__init__ import __author_email__ as author_email
from almapipy.__init__ import __project_url__ as url
from almapipy.__init__ import __project_description__ as description
from almapipy.__init__ import __license__ as license


setup(
    name = "almapipy",
    version = version,
    author = author,
    author_email = author_email,
    url = url,
    description = description,
    long_description = long_description,
#    long_description_content_type = "text/markdown",
    install_requires = ['requests'],
    keywords = 'alma exlibris exlibrisgroup api bibliographic',
    packages=find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license = license,
)
