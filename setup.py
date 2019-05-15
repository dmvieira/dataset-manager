# encoding: utf-8

from setuptools import setup, find_packages
from dataset_manager.__version__ import number
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="dataset_manager",
    version=number,
    description="Manage and automatize datasets for data science projects.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Diogo Munaro Vieira",
    author_email="diogo.mvieira@gmail.com",
    license='Apache 2',
    install_requires=[
        "PyYAML>=3.13",
        "pandas>=0.19.2",
        "fs<2.5.0",
        "fs.archive<0.7.0"
    ],
    packages=find_packages(),
)
