from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser=Browser('chrome',**executable_path, headless=False)
    return browser

def scrape():
    #---Mars News---------------------------------------------------------------------------
    browser = init_browser()
    
    final_results = {}

    #url
    url_title="https://mars.nasa.gov/news/"
    browser.visit(url_title)

    time.sleep(1)

    #Scrape page into soup
    html=browser.html
    soup=bs(browser.html,'html.parser')

    #Get title from browser
    results_title=soup.find_all('div', class_='content_title')
    news_title=results_title[1].text

    #Store data in a dictionary
    #results = {"title": news_title}

    #Quit browser after scraping
    browser.quit()

    #Create dictionary
    final_results["title"]=news_title

    #----Mars Para--------------------------------------------------------------------------
    browser = init_browser()
    
    #url
    url_para="https://mars.nasa.gov/news/8805/moxie-could-help-future-rockets-launch-off-mars/"
    browser.visit(url_para)

    time.sleep(1)

    #Scrape page into soup
    html=browser.html
    soup=bs(browser.html,'html.parser')

    #Get para from browser
    news_p=soup.find('div', class_='wysiwyg_content').\
    find('p').text

    #Store data in a dictionary
    #results2 = {"para": news_p}

    #Quit browser after scraping
    browser.quit()
    
    #Create dictionary
    final_results["para"]=news_p
    
    #-------Featured Image-----------------------------------------------------------------------
    browser = init_browser()

    #url
    url_image = 'https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA24247'
    base_url_img='https://www.jpl.nasa.gov'

    browser.visit(url_image)

    time.sleep(1)

    #Scrape page into soup
    html=browser.html
    soup=bs(browser.html,'html.parser')

    #Image results
    featured_image=soup.find_all('figure', class_='lede')

    for image in featured_image:
        i=image.find('img')
        featured_image_url=(base_url_img+i["src"])

    #Create dictionary
    #results3 = {"img_url": featured_image_url}
    final_results["img_url"]=featured_image_url
 
    #Quit browser after scraping
    browser.quit()


    #-------Facts Table-----------------------------------------------------------------------
    browser = init_browser()
    
    url_facts="https://space-facts.com/mars/"

    browser.visit(url_facts)

    time.sleep(1)

    html=browser.html
    soup=bs(browser.html,'html.parser')

    #Table data
    df=pd.read_html(url_facts,attrs = {'class':'tablepress-id-p-mars'})
    data=df[0]

    table_data={}
    for row in data.iterrows():
        key=str.replace(row[1][0],":","")
        table_data[key]=row[1][1]
#print(table_data)

    #Store data in a dictionary
    final_results["table_data"]=table_data
    #final_results.append(table_data)

    #Return results
    return final_results