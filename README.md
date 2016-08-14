# yachtworld-crawler

## Prerequisites
- Scrapy (for site grabbing)
- ipython notebook/pandas/json/etc - to Excel conversion

## how to use crawler

1) put your YW search string to SEARCH_URL, file yachtworldcrawler/yachtworldcrawler/spiders/yachtworld.py (or you can keep default)
2) cd yachtworldcrawler/yachtworldcrawler
3) scrapy crawl -o yachts.json
4) PROFIT!

## how to convert to excel

1) open ipython notebook ./yw-analyzer.ipynb
2) correct IN_PATH/OUT_PATH in step 2
3) run all
4) PROFIT!