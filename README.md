# bfcm - A statical tool written in Python.

## Description

The bfcm calculates a conditional probability of a category given a document.

## Requirement

- OS: Linux or macOS
- Python3

## Usage

1. Change directory into extracted bfcm directory in your terminal.
2. Make a directory (e.g. docs) in bfcm/mcs directory.
3. Make a documents (e.g. doc1.txt, doc2.txt and, doc3.txt) in bfcm/mcs/docs.
4. Make a tab separated CSV file judge.csv in bfcm/mcs/docs. The name judge.csv is configured in bfcm/etc/bfcm.json file.
5. Add document names and categories (e.g. vegetable	food) into judge.csv.
6. Change directory into 'top' bfcm directory agein.
7. run './init.sh'
8. run './train.sh docs'
9. run './prob.sh docs vegetable food'
10. The conditional probability of 'food' category given document 'vegetable' would be printed.

## Installation

1. Download bfcm as a zip file form bfcm repository page (https://github.com/jiyucho9145/bfcm).
2. Extract the zip file.

## Author
jiyucho9145

## Lisence
MIT
