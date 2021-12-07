# Initial setup.py template taken from:
#   https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="richzhangs",
    version="0.1.1",
    description="Rich Zhangs!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://testapp.readthedocs.io/",
    author="Yajie Zhang, Minglun Zhang",
    author_email="richzhangs@protonmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["testapp"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "dash", "waitress"]
)
