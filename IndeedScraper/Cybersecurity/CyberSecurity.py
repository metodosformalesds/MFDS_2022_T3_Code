#CyberSecurity
import time
#allows to work with time in Python. It allows functionality like getting the current time, pausing the Program from executing
from selenium import webdriver
#Selenium WebDriver is an automation testing tool. When I say automation, it means it automates test scripts written in Selenium. Webdriver Install. Chrome
import re
#A regular expression (or RE) specifies a set of strings that matches it; the functions in this module let you check if a particular string matches a given regular expression (or if a given regular expression matches a particular string
import os
#The OS module in Python provides functions for creating and removing a directory (folder), fetching its contents, changing and identifying the current directory, etc. You first need to import the os module to interact with the underlying operating system
import csv
#The Import-Csv cmdlet creates table-like custom objects from the items in CSV files.
from datetime import datetime
#imports all the content from the datetime module, but requires you to precede names that are imported from that module with the datetime. qualifier in your code.
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import pandas as pd
#The import pandas portion of the code tells Python to bring the pandas data analysis library into your current environment
from pandas_profiling import ProfileReport

from time import sleep
#Python time sleep function is used to add delay in the execution of a program
from datetime import date
#datetime in Python is the combination between dates and times.


from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title


os.chdir(r'data/mfds/mx/ds/')
#where the data is going to be saved


def get_url(position, location):
    template = 'https://mx.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url


"""
    This function simply goes to the position and location part of the website to find the designaded postions and location and the 
    Generates url postion and location 
 """


def save_data_to_file(records):
    """Save data to csv file"""
#here is where you save the file as a csv
    with open('results_2022_11_14.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'Summary', 'JobUrl'])
        writer.writerows(records)
    df = pd.DataFrame (records, columns = ['job_title', 'company', 'location', 'post_date', 'summary', 'job_url'])
    #this is the data that we want to get for  our csv

"""
    This function save the data in a csv file with the name that we already pretermined 
    with the records that we choose to get like for example ´company´
"""

def get_record(card):
    """Extract job data from single card"""
    job_title = card.find_element_by_class_name('jcs-JobTitle').text
    company = card.find_element_by_class_name('companyName').text
    location = card.find_element_by_class_name('companyLocation').text
    post_date = card.find_element_by_class_name('date').text
    summary = card.find_element_by_class_name('job-snippet').text
    job_url = card.find_element_by_class_name('jcs-JobTitle').get_attribute('href')
    return (job_title, company, location, post_date, summary, job_url)
#Extracts the data from the card

"""
    This function extracts the job data from the single card and find the element from that selected card
"""


def get_page_records(cards, job_list, url_set):
    """Extract all cards from the page"""
    for card in cards:
        record = get_record(card)
        # add if job title exists and not duplicate
        if record[0] and record[-1] not in url_set:
            job_list.append(record)
            url_set.add(record[-1])

"""
    This function extracts the job data from the single card and find the element from that selected card
"""

            
def main(position, location):
    """Run the main program routine"""
    scraped_jobs = []
    scraped_urls = set()
    
    url = get_url(position, location)
    
    #setup web driver
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

"""
    This function runs the main program  
"""

main('CyberSecurity', 'remoto')

"""
this function takes this selected jobs that we want and put it in the postirion and location     
"""
