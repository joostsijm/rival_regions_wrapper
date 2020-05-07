import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rival_regions_wrapper",
    version="0.1.0",
    author="Joost Sijm",
    author_email="joostsijm@gmail.com",
    description="Rival Regions API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjoo914/rival_regions_calc",
    packages=setuptools.find_packages(),
    install_requires=[
       'webbot',
       'cfscrape'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
