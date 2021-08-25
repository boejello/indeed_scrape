import requests
from bs4 import BeautifulSoup

position = 'construction engineer'
location = 'chicago il'
pageMax = 5

def get_url(position, location, page): # Generate url from position and location and start page
    template = 'https://www.indeed.com/jobs?q={}&l={}&radius=10&sort=date&start={}0'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    page = str(page)
    url = template.format(position, location, page)
    return url

urls = []
print(f' Getting {pageMax } urls for {position} in {location}')
for page in range(0,pageMax): # Get list of urls
    urls = get_url(position, location, page)
    response = requests.get(urls)
    soup = BeautifulSoup(response.content, 'html.parser')
    if page == 0:
        print("1st Page:", urls)
    else:
        print("Page", page+1, ":", urls )
print("-----")


def get_all_jobs():
    jobIndex = 1
    easyApplyIndex = 1
    for urls in range(0,pageMax): # Get job info from multiple urls
        for listing in soup.select('.result'): # Get job info from single url
            jobName = listing.select_one('.jobTitle').get_text(' ')
            company = listing.select_one('.companyName').get_text(' ')
            location = listing.select_one('.companyLocation').get_text(' ')
            print("#", jobIndex)
            try:
                easyApply = listing.select_one('.ialbl.iaTextBlack').get_text(' ')
                print(f'{easyApply} #{easyApplyIndex}')
                easyApplyIndex +=1
            except:
                AttributeError
            jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
            print(jobName,"-", location)
            print(company, jobLink)
            print("-----")
            jobIndex +=1


def get_easy_apply_jobs():
    jobIndex = 1
    easyApplyIndex = 1
    for urls in range(0,pageMax): # Get job info from multiple urls
        for listing in soup.select('.result'): # Get job info from single url
            jobName = listing.select_one('.jobTitle').get_text(' ')
            company = listing.select_one('.companyName').get_text(' ')
            location = listing.select_one('.companyLocation').get_text(' ')
            try:
                print("-----")
                print("#", jobIndex)
                easyApply = listing.select_one('.ialbl.iaTextBlack').get_text(' ')
                print(f'{easyApply} #{easyApplyIndex}')
                jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
                print(jobName, "-", location)
                print(company, jobLink)
                easyApplyIndex +=1
            except:
                AttributeError
            jobIndex +=1



def get_easy_apply_links():
    jobIndex = 1
    easyApplyIndex = 1
    for urls in range(0,pageMax): # Get job info from multiple urls
        for listing in soup.select('.result'): # Get job info from single url
            jobName = listing.select_one('.jobTitle').get_text(' ')
            company = listing.select_one('.companyName').get_text(' ')
            location = listing.select_one('.companyLocation').get_text(' ')
            try:
                easyApply = listing.select_one('.ialbl.iaTextBlack').get_text(' ')
                jobLink = f'https://indeed.com/viewjob?jk={listing["data-jk"]}'
                print(f'#{easyApplyIndex} - {easyApply} - {jobName} - {jobLink}')
                easyApplyIndex +=1
            except:
                AttributeError
            jobIndex +=1


def main():
    job_prompt = input(f'GET ALL JOBS ENTER A '
                       f'GET EASY APPLY JOBS ENTER B'
                       f'GET EASY APPLY LINKS ENTER C').upper()
    if job_prompt == "A":
        get_all_jobs()
    elif job_prompt == "B":
        get_easy_apply_jobs()
    elif job_prompt == "C":
        get_easy_apply_links()
    else:
        print("INVALID INPUT, TRY AGAIN")
        quit()

main()

