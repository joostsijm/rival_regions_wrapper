"""Setup file"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="rival_regions_wrapper",
    version="0.1.0",
    author="Joost Sijm",
    author_email="joostsijm@gmail.com",
    description="Rival Regions API wrapper",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="git@github.com:jjoo914/rival_regions_wrapper.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'appdirs',
        'beautifulsoup4'
        'cfscrape',
        'requests',
        'webbot',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
