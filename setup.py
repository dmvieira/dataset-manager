# encoding: utf-8

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

with open(path.join(this_directory, 'version.txt')) as f:
    version = f.readline()

setup(
    name="dataset_manager",
    version=version,
    description="Manage and automatize datasets for data science projects.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Diogo Munaro Vieira",
    author_email="diogo.mvieira@gmail.com",
    license='Apache 2',
    install_requires=[
        "PyYAML>=3.13",
        "fs<2.5.0",
        "fs.archive<0.7.0",
        "requests",
        "PTable==0.9.2"
    ],
    packages=find_packages(),
)
