# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
# 1. Initialize the browser.
# 2. Create a data dictionary.
# 3. End the WebDriver and return the scraped data.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path ={'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph":news_paragraph,
        "featured_image": featured_image(browser),
        "facts":mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_images(browser)
        }
    # Stop webdriver and return data
    browser.quit()
    return data
# add broswer in(), telling Python well use browser variable outside the function
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # optional delay for loading the page 
    browser.is_element_present_by_css('div.list_text',wait_time=1)

    html = browser.html
    news_soup = soup(html,'html.parser')
    # css, from last block, works from right to left. we also use select_one which will get the first tag
    # match a particular cirteria
    # Add try/except for error handling
    try: 
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as "news_title"
        # originally news_title is in the draft and now we are going to put the result of mars_news(the function) under 'return'
        news_title = slide_elem.find('div',class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        # originally news_p is in the draft and now we are going to put the result of mars_news(the function) under 'return'
        news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
    except AttributeError:
        # None means return nothing
        return None, None
    #news_p
    # return for function mars_news
    return news_title, news_p
# ### Feature Images
def featured_image(browser):
    # Visit URL
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html,'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url =f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url
    return img_url
### Mars facts
def mars_facts():
    # Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        # Assign columns and set index of dataframe
        df.columns=['description','Mars','Earth']
        df.set_index('description', inplace = True)
        #df
    except BaseException:
        return None
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def hemisphere_images(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = soup(html,'html.parser')
    # # 2. Create a list to hold the images and titles.
        #hemisphere_image_urls = [{"img_url":img_url,"title":title}]
    try:
        hemisphere_image_urls = []
        # # 3. Write code to retrieve the image urls and titles for each hemisphere.
        # First, get a list of all of the hemispheres
        links = browser.find_by_css('a.product-item img')
        # Next, loop through those links, click the link, find the sample anchor, return the href
        for i in range(len(links)):
            hemisphere = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
            browser.find_by_css('a.product-item img')[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
            sample_elem = browser.links.find_by_text('Sample').first
            hemisphere['img_url'] = sample_elem['href']
        
        # Get Hemisphere title
            hemisphere['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
            hemisphere_image_urls.append(hemisphere)
            #print(hemisphere['title'])
        # Finally, we navigate backwards
            browser.back()
    except AttributeError:
        return None     
        # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls
  
#browser.quit(move to scrape_all function)


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

