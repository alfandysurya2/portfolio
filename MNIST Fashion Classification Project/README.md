# MNIST-Fashion-Binary-and-Multiclass-Classification

## Project Overview
Hello! welcome to my #1 personal project. In this project i'm going to showcase how to perform several types of machine learning (ML) classification task like binary and multi-class classification using Fashion MNIST open source dataset. The main focus of this project is to:

* Performed basic binary and multi-class ML classification and explaining what differentiates between the two to classify fashion type.
* Showcased and interpreted some useful performance measures for classification task like confusion matrix, precision, recall, roc-auc, etc.
* Lastly, in this project isn't trying to create outstanding and sophisticated ML models with perfect recall and/or precision. But, this project is ultimate goal is to introduce first and second point above.

## Dataset
As already mentioned on project overview, in this project we're using [Fashion MNIST dataset](https://www.kaggle.com/datasets/zalando-research/fashionmnist) from Kaggle. Fashion MNIST is great to showcase both binary and multi-class classification because of less-complicated features or attribute that this dataset has. The dataset consist of 60.000 rows of training and 10.000 rows of test dataset. Each point of data consist 28x28 grayscale image,associated with 10 fashion label. That means it has 784 columns (each column represent 1 pixel of fashion image) + 1 label column. Each training and test example is assigned to one of the following labels:

* 0 = `T-shirt/top`
* 1 = `Trouser`
* 2 = `Pullover`
* 3 = `Dress`
* 4 = `Coat`
* 5 = `Sandal`
* 6 = `Shirt`
* 7 = `Sneaker`
* 8 = `Bag`
* 9 = `Ankle boot`

TL;DR:

* Each row is a separate image
* Column 1 is the class label.
* Remaining columns are pixel numbers (784 total).
* Each value is the darkness of the pixel (1 to 255)

## Requirements
This projcet running on Python 3.9.12 with some dependencies you're need to install. Here's the list of the dependencies:

1. [scikit-learn](https://scikit-learn.org/) ver 1.0.2
2. [pandas](https://pandas.pydata.org/) ver 1.4.2
3. [opendatasets](https://github.com/JovianHQ/opendatasets) ver 0.1.22
4. [seaborn](https://seaborn.pydata.org/) ver 0.11.2
5. [xgboost](https://xgboost.readthedocs.io/en/stable/) ver 1.7.2
6. [lightgbm](https://lightgbm.readthedocs.io/en/v3.3.2/) ver 3.3.4
7. [lazypredict](https://lazypredict.readthedocs.io/en/latest/) ver 0.2.12

Don't worry, all required dependencies is already listed in `requirement.txt` and automatically installed in the notebook.

## How to Use?
1. Install Anaconda Navigator to use Jupyter Notebook
2. Open `mnist_fashion_binary_and_multiclass_classification.ipynb`
3. Run all cell, run one by one, or just scroll through the notebook you choose!
4. You need to input your kaggle credential to download the dataset. 
<img src='images/kaggle prompt.png'> To get your credential, you need to create kaggle account first, then select account setting. In account setting, head to API section. Click on 'Create New API Token' to download your credential as 'kaggle.json' file. Open the file and you will find your username and key to download the dataset.

5. You're set!


## Notes:
1. The `fashion-mnist_train.csv` and `fashion-mnist_test.csv` file is not present in the repo because of storage limitation. Both are being downloaded straight from kaggle when you run the notebook. 
2. `fashion-mnist_test.csv` file is not used in this project. You can use it for cross validation if you want to!
4. Feel free to contribute in this project!