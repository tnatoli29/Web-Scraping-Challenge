#Import Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

def init_browser():
    #Set path to chromedriver
    executable_path = {'executable_path': 'C:/webdrivers/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

#Create a Python dictionary to be uploaded to a MongoDB
mars_info = {}

#Get Mars News
def scrape():
    #Set browser
    browser = init_browser()

    #URL we will scrape
    first_url = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    response = requests.get(first_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Get the title from the URL page
    news_title = soup.find('title')
    news_title = news_title.text

    # Get the first paragraph from the URL
    news_p = soup.find('p')
    news_p = news_p.text



    # Find the featured image for the second URL
    sec_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(sec_url)

    # HTML Object
    img_html = browser.html

    # Parse HTML
    soup = bs(img_html, "html.parser")

    # Retrieve background-image url from style tag
    img_url = soup.find('article')['style'].replace('background-image: url(', '').replace(');', '')[1:-1]

    #Use f string to combine urls
    img_url = f"https://www.jpl.nasa.gov{img_url}"


    # Find the facts about Mars using Pandas
    third_url = "https://space-facts.com/mars/"
    browser.visit(third_url)

    # Set up table
    table = pd.read_html(third_url)
    mars_table = table[1]
    mars_table.drop("Earth", inplace=True, axis=1)
    mars_table.columns = ["Statistics", "Mars"]


    #Convert table from pandas to html
    html_mars_table = mars_table.to_html()


    # Find information on Mars's hemispheres
    fourth_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(fourth_url)

    # HTML Object
    hemi_html = browser.html

    # set up soup variable
    hemi_soup = bs(hemi_html, "html.parser")

    # Set up empty list
    hemisphere_image_urls = []

    # Use Beautiful Soup to find narrow down our search
    results = hemi_soup.find("div", class_="result-list")
    hemispheres = results.find_all("div", class_="item")

    # Create for loop to get enhanced image url
    for hemi in hemispheres:
        title = hemi.find("h3").text
        title = title.replace("Enhanced", "")
        link = hemi.find("a")["href"]
        full_link = f"https://astrogeology.usgs.gov/{link}"
        browser.visit(full_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})


    #store data in dictionary
    mars_info = {
        "news_title": news_title,
        "news_p" : news_p,
        "img_url": img_url,
        "mars_facts": html_mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_info

