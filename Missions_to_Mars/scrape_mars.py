# dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Mars News

def init_browser():
    
    # establish path/connect to chrome browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    # call init_browser function
    browser = init_browser()

    # open NASA Mars News site
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)


    # parse HTML
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')  

    # use .select_one to find first search element
    mars_first_li_slide = mars_soup.select_one("ul.item_list li.slide")

    # use .find to get title from container
    mars_title = mars_first_li_slide.find("div", class_="content_title").get_text()

    # use .find to get paragraph text from continer 
    mars_paragraph = mars_first_li_slide.find("div", class_="article_teaser_body").get_text()

    # NASA JPL

    # open the NASA JPL (Jet Propulsion Laboratory) Site
    jpl_url = "https://www.jpl.nasa.gov/images/?search=&category=Mars"
    browser.visit(jpl_url)

    # hint from andrew m.
    jpl_hint = browser.find_by_css('div[class="SearchResultCard"]')
    jpl_hint[0].click()

    #parse JPL HTML
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html,"html.parser")

    # Find the relative image url
    url_image = jpl_soup.find_all('img', class_ = 'BaseImage')[0]
    jpl_url_image = url_image['data-src']



    #Mars Facts

 
    # read html into panda data frame
    mars_facts_url = 'http://space-facts.com/mars/'
    mars_facts_df = pd.read_html(mars_facts_url)

    # define columns
    mars_facts_df.columns=["Description", "Value"]
    mars_facts_df.set_index("Description", inplace=True)
    
    # insert table into HTML table
    mars_facts_table = mars_facts_df.to_html(classes='table table-striped')


    #USGS Astrogeolgy Site


    # open USGS Astrogeology Site
    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_url)
    
    # set up variables
    main_url = 'https://astrogeology.usgs.gov'
    USGS_url_images = []

    # parse USGS HTML
    USGS_html = browser.html
    USGS_soup = BeautifulSoup(USGS_html, 'html.parser')

    # scrape with bs
    items = USGS_soup.find_all('div', class_='item')

    # loop through list
    for item in items:

        # title into variable
        title = item.find('h3').text

        # link to full image
        img_url = item.find('a', class_='itemLink product-item')['href']

        # visit the site
        browser.visit(main_url + img_url)

        # parse HTML
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')

        # search, find, and store image urls
        img_url2 = main_url + soup.find('img', class_='wide-image')['src']
        USGS_url_images.append({"title": title, "image_url": img_url2})

    # store data in a dictionary
    mars_data = {
        "news_title": mars_title,
        "news_paragraph": mars_paragraph,
        "featured_image": jpl_url_image,
        "mars_facts": mars_facts_table,
        "hemispheres": USGS_url_images
    }

    # close browser
    browser.quit()

    # return dictionary
    return mars_data


