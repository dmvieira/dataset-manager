# Dataset Manager

Manage and automatize your datasets for your project with YAML files.


[![Build Status](https://travis-ci.com/dmvieira/dataset-manager.svg?branch=master)](https://travis-ci.com/dmvieira/dataset-manager)

Current Support: [![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

## How it Works

This project create a file called *identifier.yaml* in your dataset directory with these fields:

```
source: https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv

description: this dataset is a test dataset

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

### Manager functions

#### Show all Datasets

Return a table with all Datasets from dataset path

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path, local_path_to_download)

manager.show_datasets()
```

#### Create a Dataset

Create a Dataset with every information you want inside dataset_path defined.

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path, local_path_to_download)

manager.create_dataset(identifier, source, description, **kwargs)
```

#### Remove a Dataset

Remove Dataset from dataset_path

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path, local_path_to_download)

manager.remove_dataset(identifier)
```

#### Prepare Datasets

Download and Unzip all Datasets

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path, local_path_to_download)

manager.prepare_datasets()
```

#### Using Multiple Filesystems

This manager is integrated with [Pyfilesystem2](https://github.com/PyFilesystem/pyfilesystem2) and you can use all [builtin](https://docs.pyfilesystem.org/en/latest/builtin.html) filesystems or with [third-party](https://www.pyfilesystem.org/page/index-of-filesystems/) extensions or [creating your own](https://docs.pyfilesystem.org/en/latest/extension.html) extension.

With Pyfilesystem2, you can download, extract and manage datasets in any place.

```
from fs.tempfs import TempFS
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path, local_path_to_download, TempFS())

manager.prepare_datasets() # all datasets will be downloaded and extracted on temporary files respecting your local_path_to_download hierarchy
```

#### Get one Dataset

Get Dataset line as dict

```
import pandas as pd
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path, local_path_to_download)

dataset = manager.get_dataset(identifier)

df = pd.read_csv(dataset.uri)
```

### Dataset functions

#### Download Dataset

Download Dataset based on source. This only download once because validates cache.
It works both with HTTP, HTTPS and FTP protocols.

```
dataset = manager.get_dataset(identifier)

dataset.download()
```

#### Unzip Dataset

Unzip Dataset based on dataset uri. It works with zip files and others from supported library: [fs.archive](https://pypi.org/project/fs.archive/)

```
dataset = manager.get_dataset(identifier)

dataset.unzip()
```

#### Prepare Dataset

Prepare Dataset combine these two before.

```
dataset = manager.get_dataset(identifier)

dataset.prepare()
```

## Contributing

Just make pull request and be happy!

Let's grow together ;)
