# Data Scraping and API Fetching Script

This Python script allows users to scrape data from a Yelp business page, fetch data via Yelp's API, and work with static datasets (CSV/JSON). The script provides three modes of operation:

1. **Static Mode**: Load and display a static dataset (CSV/JSON).
2. **Scrape Mode**: Scrape a business page from Yelp for specific data.
3. **Default Mode**: Scrape a business page, fetch data via Yelp's API, and combine both into a CSV file.

## Requirements

For this project you are required to have any of the python environment setup.

### Python Packages

Before running the script, make sure you have the required Python packages installed. You can install the required packages using `pip` or `pip3` depending on the version you are using:

## Execution Time for each mode

**Time taken for Static Mode: 2.05 seconds**
**Time taken for Scrape Mode: 1.41 seconds**
**Time taken for Static Mode: 0.08 seconds**

```bash
pip install pandas beautifulsoup4 requests

python3 datascience.py # to run in default mode

python3 datascience.py --scrape # to run in scrape mode

python3 datascience.py --static /path/to/dataset # to run in static mode
```
