import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gphotospy",
    version="0.1.2",
    description="Unofficial Google Photos Python library ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/davidedelpapa/gphotospy",
    author="Davide Del Papa",
    author_email="davidedelpapa@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["gphotospy"],
    include_package_data=True,
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "oauth2client"
    ],
)
