"""Setup file"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="rival_regions_wrapper",
    version="1.3.2",
    author="Joost Sijm",
    author_email="joostsijm@gmail.com",
    description="Rival Regions API wrapper",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/joostsijm/rival_regions_wrapper",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "appdirs",
        "beautifulsoup4",
        "cfscrape",
        "python-dateutil",
        "pathlib2",
        "requests",
        "selenium-stealth",
        "webbot",
        "python-anticaptcha",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
