from bs4 import BeautifulSoup
import requests
import time
import csv

csv_file = open('scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Job Title', 'Company Name', 'Skills', 'Job Link'])

def find_jobs():
    for i in range(2):
        html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=software&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=software&pDate=I&sequence=1&startPage={i+1}').text
        soup = BeautifulSoup(html_text, 'lxml')

        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

        for index, job in enumerate(jobs):
            job_title = job.find('h2').text.replace('( ', '(').replace(' )', ')')
            company_name = job.find('h3', class_='joblist-comp-name').text.replace('(More Jobs)', '')
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
            csv_writer.writerow([job_title.strip(), company_name.strip(), skills.strip(), more_info])
            print(f'Job Posting for {job_title.strip()} saved')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
        print('')
    
csv_file.close()