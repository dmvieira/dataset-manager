# Dataset Manager

Manage and automatize your datasets for your project with YAML files.

Create a file *name.yaml* with content in your dataset directory:

```
name: your_dataset_name

src: https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv

description: this dataset is a test dataset

format: csv
```

*name*: is the name for dataset reference.

*src*: is location from dataset.

*description*: describe your dataset to remember later.

*format*: pandas read format following `read_<format>` as described here: https://pandas.pydata.org/pandas-docs/stable/reference/io.html.

Each dataset is a YAML file inside dataset directory.

## List all Datasets

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.list_datasets() ## return a List with all datasets from dataset path
```

## Get one Dataset

```
from dataset_manager import DatasetManager

manager = DatasetManager(dataset_path)

manager.get_dataset(name) ## Get dataset as Pandas DataFrame
```