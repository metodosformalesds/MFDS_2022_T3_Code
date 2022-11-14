import time
from selenium import webdriver
import re
import os
import csv
from datetime import datetime
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import pandas as pd
from pandas_profiling import ProfileReport

from time import sleep
from datetime import date


# In[2]:


from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title


# In[ ]:


os.chdir(r'data/mfds/mx/ds/')


# In[ ]:


def get_url(position, location):
    """Generate url from position and location"""
    #template = 'https://ca.indeed.com/jobs?q={}&l={}'
    template = 'https://mx.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url


# In[ ]:


def save_data_to_file(records):
    """Save data to csv file"""
    with open('results_2022_11_04.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'Summary', 'JobUrl'])
        writer.writerows(records)
    df = pd.DataFrame (records, columns = ['job_title', 'company', 'location', 'post_date', 'summary', 'job_url'])


# In[ ]:


def get_record(card):
    """Extract job data from single card"""
    job_title = card.find_element_by_class_name('jcs-JobTitle').text
    company = card.find_element_by_class_name('companyName').text
    location = card.find_element_by_class_name('companyLocation').text
    post_date = card.find_element_by_class_name('date').text
    summary = card.find_element_by_class_name('job-snippet').text
    job_url = card.find_element_by_class_name('jcs-JobTitle').get_attribute('href')
    return (job_title, company, location, post_date, summary, job_url)


# In[ ]:


def get_page_records(cards, job_list, url_set):
    """Extract all cards from the page"""
    for card in cards:
        record = get_record(card)
        # add if job title exists and not duplicate
        if record[0] and record[-1] not in url_set:
            job_list.append(record)
            url_set.add(record[-1])


# In[ ]:


def main(position, location):
    """Run the main program routine"""
    scraped_jobs = []
    scraped_urls = set()
    
    url = get_url(position, location)
    
    # setup web driver
    driver = webdriver.Chrome()
    driver.get(url)        
    driver.implicitly_wait(10)
    # extract the job data
    while True:
        cards = driver.find_elements_by_class_name('job_seen_beacon')
        get_page_records(cards, scraped_jobs, scraped_urls)
        try:
            driver.find_element_by_xpath('//a[@aria-label="Next Page"]').click()
        except NoSuchElementException:
            break
        except ElementNotInteractableException:
            driver.find_element_by_id('popover-x').click() 
            get_page_records(cards, scraped_jobs, scraped_urls)
            continue
    # close driver and save records
    driver.quit()
    save_data_to_file(scraped_jobs)


# In[ ]:


main('data science', 'remoto')
