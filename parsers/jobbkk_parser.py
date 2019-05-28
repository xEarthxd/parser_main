#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobbkk_parser(file_name):
    
    ## functions
    
    def get_date(soup):
        date_raw = soup.find('div', itemprop = 'datePosted').get_text()
        date_raw = date_raw.split('-')
        date = datetime.datetime(year = int(date_raw[0]), month = int(date_raw[1]), day = int(date_raw[2]))
        return date

    def get_title(soup):
        title_th = soup.find('h2', class_ = 'company-content-title').get_text()
        return title_th

    def get_description(soup):
        description = soup.find('div', itemprop = 'responsibilities').get_text().replace('\n','').replace('\t','').strip()
        return description

    def get_qualification(soup):
        qualification = soup.find('h2', text="คุณสมบัติเพิ่มเติม").next_sibling.next_sibling.get_text().replace('\n', '').replace('\t', '').strip()
        return qualification

    def get_education(soup):
        education = []
        edu_dict = {}
        edu_dict['degree'] = soup.find('span', itemprop="educationRequirements").get_text()
        edu_dict['major'] = ''
        edu_dict['faculty'] = ''
        education.append(edu_dict)
        return education

    def get_location(soup):
        location = soup.find('b', text = 'สถานที่ปฏิบัติงาน :').next_sibling.next_sibling.get_text()
        return location

    def get_company(soup):
        company = soup.find('h1', itemprop = 'hiringOrganization').get_text()
        return company

    def get_amount(soup):
        amount = soup.find('span', class_ = 'count-position').get_text()
        return amount

    def get_exp(soup):
        exp = soup.find('b', text = 'ประสบการณ์(ปี) : ').next_sibling.get_text()
        return exp

    def get_gender(soup):
        gender = gender = soup.find('b', text = 'เพศ : ').next_sibling.get_text()
        return gender

    def get_salary(soup):
        salary = soup.find('b', text = 'เงินเดือน(บาท) :').next_sibling.next_sibling.get_text()
        return salary
    
    ### parsing starts here
    
    with open(file_name, 'rb') as fin:
        soup = BeautifulSoup(fin.read(), features = "html.parser")

    try:
        date = get_date(soup)
    except:
        date = 'Not Found'

    try:
        title_th = get_title(soup)
    except:
        title_th = 'Not Found'

    try:
        description = get_description(soup)
    except:
        description = 'Not Found'

    try:
        qualification = get_qualification(soup)
    except:
        qualification = 'Not Found'

    try: 
        education = get_education(soup)
    except:
        education = 'Not Found'

    try:
        location = get_location(soup)
    except:
        location = 'Not Found'

    try:
        company = get_company(soup)
    except:
        company = 'Not Found'

    try: 
        amount = get_amount(soup)
    except: 
        amount = 'Not Found'

    try:
        exp = get_exp(soup)
    except:
        exp = 'Not Found'

    try:
        gender = get_gender(soup)
    except:
        gender = 'Not Found'

    try:
        salary = get_salary(soup)
    except:
        salary = 'Not Found'

    job_parsed = {
        "file_name" : file_name,
        "date": date,
        "title_en": '',
        "title_th": title_th,
        "description": description,
        "qualification": qualification,
        "education": education,
        "location": location,
        "company": company,
        "amount": amount,
        "exp": exp,
        "gender": gender,
        "salary": salary
        }

    return job_parsed
    
    

