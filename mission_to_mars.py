from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    title = soup.find("div", class_="content_title").text
    para = soup.find("div", class_="article_teaser_body").text

 # JPL Mars Space Image - Featured Image
    
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("footer")
    image = image.find("a")["data-fancybox-href"]
    image = "https://www.jpl.nasa.gov" + image

#Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find("p", class_ = "tweet-text").get_text().strip()

#Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace = True)
    table_html = mars_df.to_html()

#Mars Hemisphere Images
    base = 'https://astrogeology.usgs.gov'
    url = base + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all("div", "item")
    links = []
    for x in items:
        extension = x.a["href"]
        link = base + extension
        links.append(link)
    hemisphere_image_urls = []  

    for x in links:
        
       
        browser.visit(x)      
        time.sleep(1)
        html = browser.html        
        soup = bs(html, 'html.parser')
        downloads = soup.find("div", class_ = "downloads")
        list_item = downloads.find("li")
        img_url = list_item.a["href"]
        content = soup.find("div", class_ = "content")
        full_title = content.find("h2", class_ = "title").get_text().strip()
        titles = full_title.split(" Enhanced")
        title = titles[0]
        img_dict = {"title": title, "img_url": img_url}
        hemisphere_image_urls.append(img_dict)

    return_dictionary = {
        'title': title,
        'para': para,
        'mars_weather': mars_weather,
        'table_html': table_html,
        'hemisphere_image_urls': hemisphere_image_urls,
    }

    return return_dictionary