# Dataset Manager

Manage and automatize your datasets for your project with YAML files.

Create a file *name.yaml* with content in your dataset directory:

[![Build Status](https://travis-ci.com/dmvieira/dataset-manager.svg?branch=master)](https://travis-ci.com/dmvieira/dataset-manager)

```
src: https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv

description: this dataset is a test dataset

format: csv
```

*name*: is the name for dataset reference is the file name with *yaml* extension.

*src*: is location from dataset.

*description*: describe your dataset to remember later.

*format*: pandas read format following `read_<format>` as described here: https://pandas.pydata.org/pandas-docs/stable/reference/io.html.

Each dataset is a YAML file inside dataset directory.

## List all Datasets

Return a List with all datasets from dataset path

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.list_datasets()
```

## Get one Dataset

Get dataset as Pandas DataFrame and accept **Pandas** read `*args` and `**kwargs`

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.get_dataset(name, *args, **kwargs)
```

## Create a Dataset

Create a Dataset inside dataset_path defined

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.create_dataset(name, src, description, format_extension)
```

## Remove a Dataset

Remove Dataset from dataset_path

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.remove_dataset(name)
```

