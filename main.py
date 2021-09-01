import requests
from bs4 import BeautifulSoup
import pandas as pd


position = 'construction engineer'
location = 'chicago il'
pageMax = 3

def get_url(position, location, page): # Generate single url from position and location and start page
    template = 'https://www.indeed.com/jobs?q={}&l={}&radius=10&sort=date&start={}0'
    position = position.replace(' ', '&20')
    location = location.replace(' ', '&20')
    page = str(page)
    url = template.format(position, location, page)
    return url

urls = [] # Generate list of urls from position and location and start page
print(f' Scraping {pageMax} urls for search term: {position} in {location}')
for page in range(0,pageMax): # Get list of urls
    url = get_url(position, location, page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls.append(url)
    if page == 0:
        print("1st Page:", url)
    else:
        print("Page", page+1, ":", url )

def get_all_jobs():
    print("get_all_jobs()")
    jobIndex = 1
    easyApplyIndex = 1
    for urls in range(0,pageMax): # Get job info from multiple urls
        for listing in soup.select('.result'): # Get job info from single url
            jobName = listing.select_one('.jobTitle').get_text(' ')
            company = listing.select_one('.companyName').get_text(' ')
            location = listing.select_one('.companyLocation').get_text(' ')
            print("Job Listing #",jobIndex)
            try:
                easyApply = listing.select_one('.ialbl.iaTextBlack').get_text(' ')
                print(f'{easyApply} # {easyApplyIndex}')
                easyApplyIndex +=1
            except:
                AttributeError
            jobIndex += 1
            jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
            print(jobName,"-", location)
            print(company, jobLink)
            print("-----")
    jobIndex +=1

def get_easy_apply_links():
    print("get_easy_apply_links()")
    jobIndex = 1
    easyApplyIndex = 1
    for urls in range(0,pageMax): # Get job info from +  multiple urls
        for listing in soup.select('.result'): # Get job info from single url
            jobName = listing.select_one('.jobTitle').get_text(' ')
            company = listing.select_one('.companyName').get_text(' ')
            try:
                easyApply = listing.select_one('.ialbl.iaTextBlack').get_text(' ')
                jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
                print(f'#{easyApplyIndex} - Easily Apply - {jobLink} - {jobName} - {company}')
                easyApplyIndex +=1
            except:
                AttributeError
            jobIndex +=1

def get_all_jobs_list():
    print("get_all_jobs_list()")
    jobIndex = 1
    list = []
    for urls in range(0,pageMax): # Get job info from multiple urls
        for listing in soup.select('.result'): # Get job info from single url
            jobName = listing.select_one('.jobTitle').get_text(' ')
            company = listing.select_one('.companyName').get_text(' ')
            location = listing.select_one('.companyLocation').get_text(' ')
            jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
            try:
                easy_Apply = listing.select_one('.ialbl.iaTextBlack').get_text(' ')
                print(f'#{jobIndex} - {jobLink} - **{easy_Apply}** - {jobName} - {company}')
            except:
                AttributeError
                print(f'#{jobIndex} - {jobLink} - {jobName} - {company}')
            jobIndex += 1


def csvExport(): # Not working right!
    df = pd.DataFrame(get_all_jobs_list(), columns=["job index", "joblink", "jobname", "company"])
    df.to_csv('list.csv', index=False)

get_all_jobs_list()
get_all_jobs()
get_easy_apply_links()
