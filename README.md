# bfcm

A conditional probability calculator.

## Description

The bfcm is a conditional probability calculator. 
It calculates a conditional probability of a category given a document by Bayesian filter.

Two shell scripts `train.sh` and `prob.sh` are mainly used for caluculation. 
The `train.sh` makes a model in a database, and `prob.sh` calculates a conditional probability using the model in the database.

## Requirement

- OS: Linux or macOS
- Python3

## Usage

1. Change directory into extracted bfcm directory in your terminal.
2. If a model corresponding to *training_data_dir_name* have not been maked yet, 
run `./train.sh training_data_dir_name` for making a model in the database.
3. Run `./prob.sh training_data_dir_name document_content category` for calculation.
4. The conditional probability of *category* given *document_content* would be printed in a terminal.

## Installation

1. Download bfcm as a zip file form bfcm repository page (https://github.com/jiyucho9145/bfcm).
2. Extract the zip file.
3. Change directory into extracted bfcm directory in your terminal.
4. Make a training data directory (e.g. `td`) in `bfcm/mcs` directory.
5. Make a documents (e.g. `td1.txt`, `td2.txt` and, `td3.txt`) in the training data directory `bfcm/mcs/td`.
6. Make a tab separated CSV file `judge.csv` in `bfcm/mcs/td` directory. The file name `judge.csv` is specified in `bfcm/etc/bfcm.json` file.
7. Add document names and categories (e.g. `td1.txt	category1`) into `judge.csv` file.
8. Change directory into 'top' bfcm directory agein.
9. Run `./init.sh` for making a database.

## Author
jiyucho9145

## Lisence
MIT
