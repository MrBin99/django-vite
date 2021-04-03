from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    README = f.read()


setup(
    name="django-vite",
    version="1.0.0",
    description="Integration of ViteJS in a Django project.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="MrBin99",
    url="https://github.com/MrBin99/django-vite",
    requires=[
        "Django (>=1.11)",
    ],
    install_requires=[
        "Django>=1.11",
    ],
)
