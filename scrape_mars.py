from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find(class_="content_title").text
    #print(news_title)
    news_p = soup.find(class_="article_teaser_body").text
    #print(news_p)

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    browser.click_link_by_partial_text('FULL IMAGE')
    featured_image_url =  'https://www.jpl.nasa.gov' + soup.find(class_="button fancybox")['data-fancybox-href']
    #print(featured_image_url)

    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather=soup.find(class_="js-tweet-text-container")\
                    .find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")\
                    .text
    #print(mars_weather)

    url4="https://space-facts.com/mars/"

    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    #print(html_table)

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls=[]
    all_items = soup.find_all(class_='item')

    for item in all_items:
        details ={}
        url = item.find('img')['src']
        title = item.find('h3').text
        details['title'] = title
        details['img_url'] = 'https://astrogeology.usgs.gov' + url
        hemisphere_image_urls.append(details)
        
    #print(hemisphere_image_urls)

    mars_data = {
                "news_title" : news_title,
                "news_p" : news_p,
                "properties" : html_table,
                "featured_image_url" : featured_image_url,
                "mars_weather" : mars_weather,
                "hemisphere_image_urls" : hemisphere_image_urls     
                }

    #print(mars_data)

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data
