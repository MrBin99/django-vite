from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    README = f.read()


setup(
    name="django-vite",
    version="3.0.4",
    description="Integration of Vite in a Django project.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="MrBin99",
    url="https://github.com/MrBin99/django-vite",
    license="Apache License, Version 2.0",
    include_package_data=True,
    packages=find_packages(),
    requires=[
        "Django (>=3.2)",
    ],
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    extras_require={"dev": ["black"]},
)
