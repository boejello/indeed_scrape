import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select

position = 'construction engineer'
location = 'chicago il'

pageList = []
for n in range(0, 5):
    pageList.append(n)

pages = pageList

def get_url(position, location, page): # Generate url from position and location and start page

    template = 'https://www.indeed.com/jobs?q={}&l={}&start={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    page = str(page)
    url = template.format(position, location, page)
    return url

for page in pages: # Get list of urls
    url = get_url(position, location, page)
    response = requests.get(url)
    print(f'{url} \n-----')

soup = BeautifulSoup(response.content, 'html.parser')

pageIndex = 1

for job in soup.select('.result'): # Get job info from url
    jobName = job.select_one('.jobTitle').get_text(' ')
    company = job.select_one('.companyName').get_text(' ')
    location = job.select_one('.companyLocation').get_text(' ')

    jobLink = f'https://indeed.com/viewjob?jk={job["data-jk"]}'
    print("Job #", pageIndex)
    print(jobName,"-", location)
    print(company, jobLink)
    try:
        salary = job.select_one('.salary-snippet-container').get_text(' ')
        print(salary)
    except AttributeError:
        pass  # no salary listed error handling
    print("-----")
    pageIndex +=1

