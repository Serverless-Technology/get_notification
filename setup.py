from setuptools import find_packages, setup

__version__ = "0.0.1"

setup(
    name="get-notifications",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "tweepy",
        "pandas",
        "python-dotenv",
        ],
)
