from selenium import webdriver
import time
import pandas as pd
import numpy as np

url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=London%2C%20England%2C%20United%20Kingdom&locationId=&geoId=100495523&f_TPR=&distance=25&f_E=2&position=1&pageNum=0'
#Setup chromedrive
wd = webdriver.Chrome(executable_path='./chromedriver.exe')
wd.maximize_window()
wd.get(url)

#Getting the number of Data Science jobs in london
no_of_jobs = int(wd.find_element('css selector', 'h1>span').get_attribute('innerText').replace(',','').replace('+',''))

i = 2
while i <= (no_of_jobs/25)+1: 
     wd.execute_script('window.scrollTo(0, document.body.scrollHeight)')
     i = i + 1
     try:
        wd.find_element_by_xpath('/html/body/main/div/section/button').click()
        time.sleep(5)
     except:
         pass
         time.sleep(5)

job_lists = wd.find_element('class name','jobs-search__results-list')
jobs = job_lists.find_elements('tag name','li') # return a list

#elements 
job_id = []
job_title = []
company_name = []
location = []
date = []
job_link = []

for job in jobs:
    job_id0 = job.get_attribute('data-id')
    job_id.append(job_id0)

    job_title0 = job.find_element('css selector', 'h3').get_attribute('innerText')
    job_title.append(job_title0)

    company_name0 = job.find_element('css selector','h4').get_attribute('innerText')
    company_name.append(company_name0)

    location0 = job.find_element('css selector', 'span.job-search-card__location').get_attribute('innerText')
    location.append(location0)

    date0 = job.find_element('css selector','div>div>time').get_attribute('datetime')
    date.append(date0)

    job_link0 = job.find_element('css selector','a').get_attribute('href')
    job_link.append(job_link0)



jd = []
seniority = []
job_func = []
industries = []



for item in range(len(jobs)):
    job_func0 = []
    industries0 = []
    
    
    job_click_path = f'//*[@id="main-content"]/section[2]/ul/li[{item+1}]'
    job_click = job.find_element('xpath', job_click_path).click()
    time.sleep(5)

    jd_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div'
    jd0 = job.find_element('xpath', jd_path).get_attribute('innerText')
    jd.append(jd0)

    seniority_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'
    seniority0 = job.find_element('xpath',seniority_path).get_attribute('innerText')
    seniority.append(seniority0)

    job_func_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span'
    job_func_elements = job.find_elements('xpath', job_func_path)
    for element in job_func_elements:
        job_func0.append(element.get_attribute('innerText'))
        job_func_final = ','.join(job_func0)
        job_func.append(job_func_final)

    industries_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span'
    industries_elements = job.find_elements('xpath', industries_path)
    for element in industries_elements:
        industries0.append(element.get_attribute('innerText'))
        industries_final = ','.join(industries0)
        industries.append(industries_final)


job_dict = {'ID': job_id,
'Date': date,
'Company': company_name,
'Title': job_title,
'Location': location,
'Description': jd,
'Level': seniority,
'Function': job_func,
'Industry': industries,
'Link': job_link
}

job_data = pd.DataFrame({key:pd.Series(value) for key, value in job_dict.items()})

job_data.head()


job_data['Description'] = job_data['Description'].str.replace('\n','')
job_data.to_excel('LinkedIn Job Data_Data Scientist.xlsx', index = False)


