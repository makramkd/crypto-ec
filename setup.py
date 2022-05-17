import os
import unittest

from setuptools import find_packages, setup

import crypto


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests/", pattern="test_*.py")
    return test_suite


setup(
    name="crypto-ec",
    version=crypto.__version__,
    description="Simple Python Crypto library",
    author="Makram Kamaleddine",
    url="https://github.com/makramkd/crypto",
    keywords="crypto elliptic curve",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    test_suite="setup.test_suite",
)
