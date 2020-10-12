import time
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import pandas as pd

chrome_options = Options()
chrome_options.add_argument('--headless')


class Driver:
    def __init__(self, driver_path: str, url: str, implicitly_wait: int = 3, headless: bool = False):

        if headless:
            options = Options()
            options.add_argument('--headless')
            options = options.to_capabilities()
        else:
            options = None

        # todo set up mapping to different types of drivers based on driver path
        self.driver = webdriver.Chrome(driver_path, desired_capabilities=options)

        self.driver.implicitly_wait(implicitly_wait)
        self.driver.get(url)


class TwitterParser(Driver):
    def __init__(self, driver_path: str, url: str, implicitly_wait: int = 3, headless: bool = False):
        super().__init__(driver_path, url, implicitly_wait, headless)

    def pull_tweets(self):
        collected_posts = list()
        df = pd.DataFrame(columns=['link', 'user', 'text'])

        posts = self.get_posts()
        # todo break this down into simpler functions
        # todo handle iteration better as it only iterates over so many tweets
        # todo add saving feature to save during iterations
        # todo possibly add feature to read past inputs and skip scrapped tweets (only if the user sets this up using a boolean)
        for x in range(100):
            print(x)
            if posts:
                current_child = str(posts.pop())
                try:
                    child_soup = BeautifulSoup(current_child, 'html.parser')
                    pattern = r'\/.*\/status\/[0-9]*'
                    completed_post = False
                    for link in child_soup.find_all('a'):
                        if re.match(pattern, str(link['href'])):
                            if link not in collected_posts:
                                collected_posts.append(link)
                                break
                            else:
                                completed_post = True
                                break

                    if completed_post:
                        continue
                    else:
                        user = child_soup.find('div', {'class': 'css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2'})
                        text = child_soup.find('div', {
                            'class': 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})
                        df = df.append({'link': collected_posts[-1]['href'], 'user': user.text.split('@')[-1].split('·')[0], 'text': text.text},ignore_index=True)

                except Exception as e:
                    print(e)
                    continue
                finally:
                    print('*' * 200)
            else:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                posts = self.get_posts()
                time.sleep(1)
        return df

        # df = pd.DataFrame(columns=data['columns'], data=data['data'])

    def get_posts(self):
        # todo set up mapping or allow change in xpath for posts; maybe determine automatically if it is user/search feed
        content = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div')
        # /html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div <- for normal search feed
        # /html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div <- for user feed

        soup = BeautifulSoup(content.get_attribute('innerHTML'), 'html.parser')
        posts = list(soup.children)

        return posts


if __name__ == '__main__':

    tweet_parser = TwitterParser('chromedriver.exe', 'https://twitter.com/cbparizona?lang=en')
    time.sleep(3)
    df = tweet_parser.pull_tweets()
    df.to_csv(f'scrapped_tweets_{time.strftime("%Y%m%d-%H%M%S")}.csv')
