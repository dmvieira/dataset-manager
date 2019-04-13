# Dataset Manager

Manage and automatize your datasets for your project with YAML files.


[![Build Status](https://travis-ci.com/dmvieira/dataset-manager.svg?branch=master)](https://travis-ci.com/dmvieira/dataset-manager)

Current Support: [![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-270/)[![Python 3.4](https://img.shields.io/badge/python-3.4-blue.svg)](https://www.python.org/downloads/release/python-340/)[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

## How it Works

This project create a file called *identifier.yaml* in your dataset directory with these fields:

```
source: https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv

description: this dataset is a test dataset

format: csv
```

*identifier*: is the identifier for dataset reference is the file name with *yaml* extension.

*source*: is location from dataset.

*description*: describe your dataset to remember later.

Each dataset is a YAML file inside dataset directory.

## Installing

With pip just:

```
pip install dataset_manager
```

With conda:

```
conda install dataset_manager
```

## Using

You can manage your datasets with a list of commands and integrate with [Pandas](https://pandas.pydata.org/) or other data analysis tool.

### List all Datasets

Return a List with all Datasets from dataset path

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.list_datasets()
```

### Get one Dataset

Get Dataset line as dict

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.get_dataset(identifier)
```

### Create a Dataset

Create a Dataset with every information you want inside dataset_path defined.

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.create_dataset(identifier, source, description, **kwargs)
```

### Remove a Dataset

Remove Dataset from dataset_path

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.remove_dataset(identifier)
```

## Contributing

Just make pull request and be happy!

Let's grow together ;)