# Ark Intel Processors Crawler
Intel Processors Crawler using Kimonolabs APIs.
This app uses Python 3 scripting.

## Usage

### Crawling Data
To crawl data from Kimonolabs, type the following script:
```python3 crawlIntelProcessor.py -p```
*Note*: Kimonolabs will automatically crawl the data weekly, so you will only need to use `-p` once a week to update.

To only reformat the data to be more readable and usable, type:
```python3 crawlIntelProcessor.py```

The crawled data will reside in `processors/` directory, in the following files:
- *raw-data.json* is the data fetched from Kimonolabs
- *formatted-data.json* is the data reformatted from **raw-data.json**

### Format Data
To format the crawled data to CSV, type the following:
```python3 formatProcessor.py <directory_of_crawled_phones_data> [True|False]```
The second argument (True|False) is optional, to set whether to scan subdirectories (True) or not (False) -- case-sensitive.

Most of the time, you will run:
```python3 formatPhone.py phones```

## Additional Notes
This project is originally created for Tokopedia usage and is now open-sourced.
Feel free to reformat the raw data to your styling by editing `src/Phone.py`