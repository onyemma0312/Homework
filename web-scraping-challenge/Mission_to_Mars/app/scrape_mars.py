#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[ ]:


mars = {}


# ## Visit the NASA mars news site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html


# In[5]:


soup = bs(html, "html.parser")


# In[6]:


news_title_all = soup.find_all("div", class_="content_title")


# In[ ]:


#scrape the latest new
news_title = news_title_all[1].text
news_title
mars["news_title"] = news_title


# In[ ]:


news_p = soup.find("div", class_="article_teaser_body").get_text()
news_p
mars["news_p"]= news_p


# ## JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[10]:


# Ask Splinter to Go to Site and Click Button with Class Name full_image
# <button class="full_image">Full Image</button>
full_image_button = browser.find_by_id("full_image")
full_image_button.click()


# In[11]:


# Find "More Info" Button and Click It
browser.is_element_present_by_text("more info", wait_time=1)
more_info_element = browser.find_link_by_partial_text("more info")
more_info_element.click()


# In[12]:


# Parse Results HTML with BeautifulSoup
html = browser.html
image_soup = bs(html, "html.parser")


# In[ ]:


img_url = image_soup.select_one("figure.lede a img").get("src")
img_url


# In[ ]:


# Use Base URL to Create Absolute URL
img_url = f"https://www.jpl.nasa.gov{img_url}"
print(img_url)
mars["featured_image_url"] = img_url


# ## Mars Weather

# In[15]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[16]:


html = browser.html
weather_soup = bs(html, 'html.parser')


# In[17]:


# Find a Tweet with the data-name `Mars Weather`
mars_weather_tweet = weather_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })


# In[18]:


# Search Within Tweet for <p> Tag Containing Tweet Text
mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
print(mars_weather)


# ## Mars Hemispheres

# In[ ]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[ ]:


hemisphere_image_urls = []

# Get a List of All the Hemispheres
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
    hemisphere_image_urls.append(hemisphere)
    
    # Navigate Backwards
    browser.back()


# In[ ]:


hemisphere_image_urls
mars["hemisphere"] = hemisphere_image_urls


# ## Mars Facts

# In[ ]:


import pandas as pd


# In[ ]:


# Visit the Mars Facts Site Using Pandas to Read
mars_df = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_df)
mars_df.columns=["Description", "Value"]
mars_df.set_index("Description", inplace=True)
mars_df
mars["facts"] = mars_df


# In[43]:


browser.quit()


# In[ ]:




