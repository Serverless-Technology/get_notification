from setuptools import find_packages, setup

__version__ = "0.0.1"

setup(
    name="cdslite",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "flask",
        "python-dotenv",
        "passlib",
        "uuid",
        "flask-sse",
        "flask_session",
        "requests",
    ],
)
