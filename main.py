import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

position = 'construction engineer'
location = 'miami fl'
pageMax = 5

print("... Now running main.py 1... ")

def get_url(position, location, page): # Generate single url from position and location and start page
    print("... Now running main.py 2... ")
    template = 'https://www.indeed.com/jobs?q={}&l={}&radius=10&sort=date&start={}0'
    position = position.replace(' ', '&20')
    location = location.replace(' ', '&20')
    page = str(page)
    url = template.format(position, location, page)
    return url

urls = []  # Generate list of urls from position and location and start page
print(f' Scraping {pageMax} urls for search term: {position} in {location}')
for page in range(0, pageMax):  # Get list of urls
    url = get_url(position, location, page)
    response = requests.get(url, headers={'Cache-Control': 'no-cache'})
    soup = BeautifulSoup(response.content, 'html.parser')
    urls.append(url)
    if page == 0:
        print("List of Easy Apply Jobs from Page 1:", url)
    else:
        print("List of Easy Apply Jobs from Page", page + 1, ":", url)

    easyApplyIndex = 1

    easyApplyIndexList = []
    jobLinkList = []
    jobNameList = []
    companyList = []

    for listing in soup.select('.result'): # Get job info from single url

        job = listing.select_one('.jobTitle').get_text(' ') # Gets job title
        jobName = job.split(' ', 1)[1] # Removes "new" from job title
        company = listing.select_one('.companyName').get_text(' ')
        jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
        try:
            listing.select_one('.ialbl.iaTextBlack').get_text(' ') # Scrapes urls for "Easy Apply"
            print(f'#{easyApplyIndex} - {jobLink} - {jobName} - {company}')
            jobLinkList.append(jobLink)
            jobNameList.append(jobName)
            companyList.append(company)
            easyApplyIndexList.append(easyApplyIndex)
            easyApplyIndex +=1
        except:
            AttributeError


    data = {'Job Index': easyApplyIndexList, 'Easy Apply Job Link': jobLinkList, 'Job Name': jobNameList, 'Company': companyList}
    df = pd.DataFrame(data, columns=['Job Index', 'Easy Apply Job Link', 'Job Name', 'Company'])
    df.to_csv('export.csv', mode='a', index=False) # Exports scraped data into csv
