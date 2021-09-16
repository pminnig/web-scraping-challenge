
def scrape():
    # Dependecies
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    from webdriver_manager.chrome import ChromeDriverManager
    import requests

    # URL's we will be scraping
    redplanet_url = 'https://redplanetscience.com/'
    spaceimg_url = 'https://spaceimages-mars.com/'
    marsfact_url = 'https://galaxyfacts-mars.com/'
    hemisphere_url = 'https://marshemispheres.com/'

    # Retrieving the pages
    redplanet_res = requests.get(redplanet_url)
    spaceimg_res = requests.get(spaceimg_url)
    marsfact_res = requests.get(marsfact_url)
    hemisphere_res = requests.get(hemisphere_url)

    # Setting up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Retrieve red planet first article title and paragraph
    browser.visit(redplanet_url)
    html = browser.html
    redplanet_soup = BeautifulSoup(html, 'html.parser')
    redplanet_results = redplanet_soup.find_all('div', class_='list_text')
    news_title = redplanet_soup.find('div', class_='content_title').text
    news_p = redplanet_soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)

    # Setting up splinter to find the featured image url
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # open the website
    browser.visit(spaceimg_url)
    # Open the featured image
    browser.links.find_by_partial_href('featured').click()
    # save the new webpage's html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find featured image extension and add it onto the base html
    featured_image_result = soup.find_all('img', class_='fancybox-image')
    featured_src = featured_image_result[0].get('src')
    featured_image = spaceimg_url + featured_src
    print(featured_image)

    # Reading in the HTML tables
    tables = pd.read_html(marsfact_url)

    # Saving the second table as a df
    mars_df = tables[1]
    mars_df = mars_df.rename(columns={0: 'Attribute', 1: 'Value'})
    mars_df = mars_df.set_index('Attribute')
    mars_table = mars_df.to_html()
    print(mars_table)

    # find the links to each hemisphere's page
    links = []
    response = requests.get(hemisphere_url)
    hemisphere_soup = BeautifulSoup(response.text, 'html.parser')
    for link in hemisphere_soup.find_all('a'):
        links.append(link.get('href'))
    hemisphere_links = [links[3],links[5],links[7],links[9]]

    # visit the links and retrieve the image url and title
    # put the title and image into a dictionary and make a list of these distionaries
    hemisphere_image_urls = []
    for link in hemisphere_links:
        response = requests.get(hemisphere_url + link)
        hemisphere_soup = BeautifulSoup(response.text, 'html.parser')
        image = hemisphere_soup.find('img', class_='wide-image')
        title = hemisphere_soup.find('h2', class_='title').text
        title = title.replace('Enhanced','')
        hemisphere_image_urls.append({'title': title, 'img_url': hemisphere_url + image.get("src")})

    

    html_dict = { 'title':news_title, 'paragraph':news_p,'f_images':featured_image, 'facts':mars_table, 'hem_urls':hemisphere_image_urls}
    return html_dict
