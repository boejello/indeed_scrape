import requests
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.support.ui import Select
from selenium import webdriver


position = 'construction engineer'
location = 'chicago il'
pageMax = 3

def get_url(position, location, page): # Generate url from position and location and start page
    template = 'https://www.indeed.com/jobs?q={}&l={}&radius=10&sort=date&start={}0'
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
    if page == 0:
        print("1st Page:", urls)
    else:
        print("Page", page+1, ":", urls )
print("-----")

pageIndex = 1

def indeedApplyTag():
    if soup.find("span", {"class": "Apply Now"}):
        print("Apply Now Tag Found!1")
    if soup.findAll(text="Apply Now"):
        print("Apply Now Tag Found!2")
    elif soup.find("td", class_='shelfItem indeedApply'):
         print("Apply Now Tag Found!3")
    elif soup.find_all("span", {"class": "Apply Now"}):
        print("Apply Now Tag Found!4")
    elif soup.find("div", {"class": "jobsearch-IndeedApplyButton"}):
        print("Apply Now Tag Found!5")
    elif soup.find_all("div", {"class": "jobsearch-IndeedApplyButton"}):
        print("Apply Now Tag Found!6")
    elif soup.find("div", {"id": "indeedApplyButtonContainer"}):
        print("Apply Now Tag Found!7")
    elif soup.find_all("div", {"id": "indeedApplyButtonContainer"}):
        print("Apply Now Tag Found!8")
    elif soup.find(itemprop="indeedApplyButtonContainer"):
        print("Apply Now Tag Found!81")
    elif job.select_one('.jobsearch-IndeedApplyButton-contentWrapper'):
        print("Apply Now Tag Found!9")
    else:
        print("Indeed Apply Tag Not Found1")


for urls in range(0,pageMax): # Get job info from multiple urls
    for job in soup.select('.result'): # Get job info from single url
        jobName = job.select_one('.jobTitle').get_text(' ')
        company = job.select_one('.companyName').get_text(' ')
        location = job.select_one('.companyLocation').get_text(' ')
        jobLink = f'https://indeed.com/viewjob?jk={job["data-jk"]}'
#if soup.find("span", class_='ialbl iaTextBlack').text == "Easily Apply":
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
        pass

