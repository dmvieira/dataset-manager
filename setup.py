# encoding: utf-8

from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dataset_manager",
    version="0.0.2",
    description="Manage and automatize datasets for data science projects.",
    long_description=long_description,
    author="Diogo Munaro Vieira",
    author_email="diogo.mvieira@gmail.com",
    license='Apache 2',
    install_requires=[
        "PyYAML==5.1",
        "pandas>=0.19.2"
    ],
    packages=find_packages(),
)
