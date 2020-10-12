# KM_TweetScraper

KM_TweetScraper is a simple tool to gather a set of tweets from a twitter feed using Selenium and BS4.

The tool makes use of Selenium to go to the site and grab the div tag that contains all the posts using 
the appropriate xpath. The innerHTML attribute is used in conjunction with BS4 and the desired HTML is ready
for parsing.
 
 The children of the scraped div are collects and iterated upon. The links of each available post are pulled 
out and checked if they are already in a list of links; if so, then the current iteration continues to the next
iteration. This is used to only collect each post once, and links of posts contain a unique post id. If the link is found
to be unique, the user and text information is pulled. These are all then appended to a pandas dataframe. If all the
child elements have been iterated upon, then Selenium will scroll down and scrap the containing div once again with
the updated elements. 

## Installation

Clone the repo and open up a terminal. CD into the directory and run:

```bash
pip install -r requirements.txt
```

## Usage
With the file scraper.py in the same directory run the following or similar:
```python
import tweet_parser
    
tweet_parser = TwitterParser('chromedriver.exe', 'https://twitter.com/cbparizona?lang=en')
time.sleep(3)
df = tweet_parser.pull_tweets()
df.to_csv(f'scrapped_tweets_{time.strftime("%Y%m%d-%H%M%S")}.csv')
```

## Road Map

Various parts of the tool need to be resolved. Future updates may include:

- More option availability for the driver (i.e. Chrome options)
- Abstracting hard-coding xpaths and class paths
- Scrape geo, pictures, time, etc..
- Set up config and main file to run tool
- Overall breakdown of functionality into more simpler functions or methods
- Saving features/feature to read file of scraped data and skip those tweets if chosen by user


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)