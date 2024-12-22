#!/bin/bash

STOCK_DATA_DIR=/data
STOCK_TEMP_DIR=/temp

YEAR=$(date -d '-1 day' +%Y)
FILE=COTAHIST_A$YEAR.ZIP
ZIP_PATH=$STOCK_TEMP_DIR/$FILE
wget --no-check-certificate -O $ZIP_PATH https://bvmf.bmfbovespa.com.br/InstDados/SerHist/$FILE
unzip -d $STOCK_TEMP_DIR -o $ZIP_PATH | grep "inflating:" | awk '{print $2}' | while read -r file; do
    sort -k1.1,1.2 -k1.3,1.10 -k1.13,1.24 $file -o $STOCK_DATA_DIR/$YEAR
done

rm $STOCK_TEMP_DIR/*
