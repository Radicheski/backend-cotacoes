#!/bin/bash

STOCK_DATA_DIR=/data
STOCK_TEMP_DIR=/temp

download_data() {
    local YEAR=$1
    local FILE="COTAHIST_A$YEAR.ZIP"
    local ZIP_PATH="$STOCK_TEMP_DIR/$FILE"

    wget --no-check-certificate -O "$ZIP_PATH" "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/$FILE"

    unzip -d "$STOCK_TEMP_DIR" -o "$ZIP_PATH" | grep "inflating:" | awk '{print $2}' | while read -r file; do
        sort -k1.1,1.2 -k1.3,1.10 -k1.13,1.24 "$file" -o "$STOCK_DATA_DIR/$YEAR"
    done
}

update() {
  local YEAR=$(date -d '-1 day' +%Y)
  download_data "$YEAR"
}

download_missing_data() {
  local START_YEAR=1986
  local END_YEAR=$(date -d '-1 day' +%Y)
  for YEAR in $(seq $START_YEAR "$END_YEAR"); do
        if [ ! -f "$STOCK_DATA_DIR/$YEAR" ]; then
            download_data "$YEAR"
        fi
    done
}

clear_temp_dir() {
  rm -f ${STOCK_TEMP_DIR:?}/*
}

mkdir -p $STOCK_DATA_DIR
mkdir -p $STOCK_TEMP_DIR

update
download_missing_data
clear_temp_dir
