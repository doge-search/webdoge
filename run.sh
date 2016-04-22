#!/bin/bash

cd ./liqian
python craw_modify.py > output6.txt

cd ../xiaoqiqi
python crawl_dblp.py > output5.txt

