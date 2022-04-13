# FFT
## Purpose
FFT of time domain scope RAW data in csv format.

## Prerequisites
The script requires the following python libraries:
- argparse
- pandas
- matplotlib
- numpy

## Description 
To check correct operation of FFT first an ideal sine wave is generated and the FFT computed. Time domain and frequency domain data are displayed in two sub plots.
Afterwards the csv-File either passed as command line argument (via switch -f) or a default file is read. Example csv-files are within the repositories.
Additionally the window function can be passed as argument (via switch -w).

Default settings are:
- file name: tek0001CH4.csv
- window function: hamming

Adapt settings for read_csv according your needs. Please note, that the column names in header row will be replaced by "time" and "val", whereas "time" represents the x-values and "val" the y-values
The correctness can be checked via print of pandas data frame head (first five data rows).


## ToDo
File error handling
