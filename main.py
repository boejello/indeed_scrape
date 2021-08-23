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
for page in range(0,pageMax): # Get list of urls
    urls = get_url(position, location, page)
    response = requests.get(urls)
    soup = BeautifulSoup(response.content, 'html.parser')
    if page == 0:
        print("1st Page:", urls)
    else:
        print("Page", page+1, ":", urls )
    easyApplyCount = len(soup.find_all("span", class_='ialbl iaTextBlack'))
    print(f"There are {easyApplyCount} Easy Apply links in this page \n-----")

pageIndex = 1
easyApplyIndex = 1

for urls in range(0,pageMax): # Get job info from multiple urls
    for listing in soup.select('.result'): # Get job info from single url
        jobName = listing.select_one('.jobTitle').get_text(' ')
        company = listing.select_one('.companyName').get_text(' ')
        location = listing.select_one('.companyLocation').get_text(' ')
        print("#", pageIndex)
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
        pageIndex +=1


