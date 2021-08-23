import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select

position = 'construction engineer'
location = 'chicago il'
pageMax = 5


def get_url(position, location, page): # Generate url from position and location and start page
    template = 'https://www.indeed.com/jobs?q={}&l={}&radius=10&sort=date&start={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    page = str(page)
    url = template.format(position, location, page)
    return url

urls = []
for page in range(0,pageMax): # Get list of urls
    urls = get_url(position, location, page)
    response = requests.get(urls)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(urls)

pageIndex = 1

for urls in range(0,pageMax): # Get job info from multiple urls
    for job in soup.select('.result'): # Get job info from single url
        jobName = job.select_one('.jobTitle').get_text(' ')
        company = job.select_one('.companyName').get_text(' ')
        location = job.select_one('.companyLocation').get_text(' ')
        jobLink = f'https://indeed.com/viewjob?jk={job["data-jk"]}'
        print("Job Listing #", pageIndex)
        print(jobName,"-", location)
        print(company, jobLink)
        try:
            salary = job.select_one('.salary-snippet-container').get_text(' ')
            print(salary)
        except AttributeError:
            pass  # no salary listed error handling
        print("-----")
        pageIndex +=1



