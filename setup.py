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
        "bot-studio",
        "google-search-results",
        "boto3",
        "python-dotenv",
        ],
)

# s3://get-notifications/google-events/2021-06-18T00:00:00.000Z.json
