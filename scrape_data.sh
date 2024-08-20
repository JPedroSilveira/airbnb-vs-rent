#!/bin/bash

OUTPUT_DIR=./data

if [ ! -d  $OUTPUT_DIR ]; then 
    mkdir "$OUTPUT_DIR"
fi

CITIES=('rj')

{
    for city in "${CITIES[@]}"; do
        echo Scraping airbnb data...
        python get_airbnb_data.py "$city" 2024-09-01 2024-12-01 -o "$OUTPUT_DIR"
        echo Scraping quinto andar data...
        python get_quinto_andar_data.py "$city" -o "$OUTPUT_DIR"
    done

} >> ./logs/scraping_$(date +%F).log 2>&1