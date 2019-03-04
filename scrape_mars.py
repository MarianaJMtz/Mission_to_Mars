def scrape():
    
    #Dependencies
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    from splinter.exceptions import ElementDoesNotExist
    import pandas as pd

    # First URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    #Retrieve latest news' title and paragraph; store into variables
    results = soup.find('div', class_='image_and_description_container')
    
    news_title = results.find_all('img')
    news_title = news_title[1]['alt']
    news_p = results.find('div', class_='rollover_description_inner').text
    news_p = news_p.replace('\n','')

    #Set up Chrome.exe
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Connect to URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Prepare to use Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Push FULL IMAGE button to retrieve the image URL
    browser.click_link_by_partial_text('FULL IMAGE')

    #Retrieve image URL
    results = soup.find('a', class_='button fancybox')
    feature_image_url = results['data-fancybox-href']
    feature_image_url = feature_image_url.replace('medium','large')
    feature_image_url = feature_image_url.replace('ip','hires')
    url_short = url.rsplit('/spaceimages',1)[0]
    feature_image_url = url_short + feature_image_url

    #Now let's retrieve Mars weather
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    #Find all the tags that contain tweets
    results = soup.find_all('div', class_='content')

    for result in results:
        texto = result.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        x= texto.find("InSight sol")
    
        if x == 0:
            mars_weather = texto.rsplit('pic.twitter',1)[0]
            break

    #Go for the FACTS table!
    url = 'https://space-facts.com/mars/'

    #Start retrieving the data from the table
    table = pd.read_html(url)

    #Organize pandas df
    df = table[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    #Transform to HTML string
    html_table = df.to_html()

    #Set up Chrome.exe
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Connect to URL to find photos of Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives'
    browser.visit(url)

    Hemispheres = ['valles_marineris', 'syrtis_major', 'schiaparelli', 'cerberus']
    hemisphere_image_urls = []

    for Hemisphere in Hemispheres:
    
        try:
            browser.click_link_by_partial_href(Hemisphere + '_enhanced' )
            #Prepare to use Beautiful Soup
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('h2', class_='title').text
            #title = title.rsplit(' Enhanced',1)[0]
            image = soup.find('img', class_='wide-image')
            image_link = 'https://astrogeology.usgs.gov' + image['src']
            d = {'title': title,'image_url' : image_link}
            hemisphere_image_urls.append(d)
        
        except:
            browser.find_link_by_text('2').first.click()
            browser.click_link_by_partial_href(Hemisphere + '_enhanced' )
            #Prepare to use Beautiful Soup
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('h2', class_='title').text
            #title = title.rsplit(' Enhanced',1)[0]
            image = soup.find('img', class_='wide-image')
            image_link = 'https://astrogeology.usgs.gov' + image['src']
            d = {'title': title,'image_url' : image_link}
            hemisphere_image_urls.append(d)
            
    results_dict = {'news_title' : news_title, 'news_p' : news_p, 'feature_image_url' : feature_image_url,\
                    'mars_weather' : mars_weather, 'html_table' : html_table, 'hemisphere_image_urls' : hemisphere_image_urls}
    return results_dict
