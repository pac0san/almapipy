#-*- coding: utf-8-unix -*-

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "1.1.0"

setup(
    name="almapipy",
    version=VERSION,
    author="Steve Pelkey",
    author_email="spelkey@ucdavis.edu",
    description="Python requests wrapper for the Ex Libris Alma API",
    long_description=long_description,
#    long_description_content_type="text/markdown",
    url="https://github.com/UCDavisLibrary/almapipy",
    install_requires=['json', 'os', 'requests', 'xml.etree.ElementTree'],
    keywords='alma exlibris exlibrisgroup api bibliographic',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
