#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobsdb_parser(file_name):
    
    ### functions
    
    def get_date(soup):
        date_raw = soup.find('p', class_='data-timestamp').text.strip().split('-')
        month_real = ''
        month_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_en = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for month in month_en:
            num = month_en.index(month)
            if date_raw[1] == month:
                month_real = month_num[num]
        
        year = int(date_raw[2]) + 2000
        date = datetime.datetime(year = int(year), month = int(month_real), day = int(date_raw[0]))
        return date
    
    def get_title(soup):
        title_th = soup.find('div', class_="primary-general-box general-posgp").find('h1').text.strip()
        return title_th
    
    def get_description(soup):
        description = soup.find('div', {'class': 'jobad-primary-details'}).text.strip().replace('\n','').replace('\t', '').replace('\r', '').replace('\xa0', '')
        return description
    
    def get_education(soup):
        education = []
        edu_dict = {}
        if soup.find('h3', text="ระดับการศึกษา") is None:
            edu_dict['degree'] = ''
        else :
            edu_dict['degree'] = soup.find('h3', text="ระดับการศึกษา").next_sibling.next_sibling.text.strip()
        
        edu_dict['major'] = ''
        edu_dict['faculty'] = ''
        education.append(edu_dict)
        return education
    
    def get_company(soup):
        if soup.find('h2', {'class':'jobad-header-company'}) is None:
            company = ''
            return company
        else:
            company = soup.find('h2', {'class':'jobad-header-company'}).text.strip()
            return company  
    
    def get_location(soup):
        if soup.find('div', class_="primary-meta-box row meta-location") is None:
            location = ''
            return location
        
        else:
            location = soup.find('div', class_="primary-meta-box row meta-location").text.strip().split(' ')[2]
            return location
    
    def get_exp(soup):
        if soup.find('div', class_='primary-meta-box row meta-exp') is None:
            exp = ''
            return exp
        else:
            exp = soup.find('div', class_='primary-meta-box row meta-exp').text.strip().split(' ')[1]
            return exp
    
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
        "amount": '',
        "exp": exp,
        "gender": '',
        "salary": ''
    }
    
    return job_parsed

