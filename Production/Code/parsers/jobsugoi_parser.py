#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobsugoi_parser(file_name):
    
    ### functions
    
    def get_date(soup):
        date_raw = soup.find('div', class_='jobinfo-update').text.strip().replace('\n','').replace('                                ',' ').split(' ')[2]
        date_raw = date_raw.split('/')
        date = datetime.datetime(year = int(date_raw[2]), month = int(date_raw[1]), day = int(date_raw[0]))
        return date
    
    def get_title(soup):
        title_th = soup.find('div', class_='title').text.strip()
        return title_th
    
    def get_description(soup):
        description = soup.find('div', class_="jobinfo-desc m-t-15").text.strip().replace('\r','').replace('\n','')
        return description
    
    def get_location(soup):
        location = soup.find('div', class_="pin").next_sibling.next_sibling.text.strip()
        return location
    
    def get_company(soup):
        company = soup.find('div', class_='company-head m-t-10').text.strip()
        return company
    
    def get_amount(soup):
        amount = soup.find('th', text="จำนวนที่รับ").next_sibling.next_sibling.text
        return amount
    
    def get_exp(soup):
        exp = soup.find('th', text="ประสบการณ์การทำงาน").next_sibling.next_sibling.text.strip().replace('\n', '').replace('\r', '').replace('                                                                                                                ', '').replace('～', ' ').strip()
        return exp
    
    def get_gender(soup):
        gender = soup.find('th', text="เพศ").next_sibling.next_sibling.text.strip().replace('\n', '').replace('\r', '').replace('                                                                                                                ', '')
        return gender
    
    def get_salary(soup):
        salary = soup.find('th', text="เงินเดือน(บาท/เดือน)").next_sibling.next_sibling.text.strip().replace('\n', '').replace('\r', '').replace('                                                                                                                ', '').replace('\t', ' ')
        salary2 = ' '.join(salary.split())
        return salary2
    
    def get_education(soup):
        education = []
        edu_dict = {}
        edu_dict['degree'] = soup.find('th', text="ระดับการศึกษา").next_sibling.next_sibling.text
        edu_dict['major'] = ''
        edu_dict['faculty'] = ''
        education.append(edu_dict)
        return education
    
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
        "qualification": '',
        "education": education,
        "location": location,
        "company": company,
        "amount": amount,
        "exp": exp,
        "gender": gender,
        "salary": salary
    }
    
    return job_parsed

