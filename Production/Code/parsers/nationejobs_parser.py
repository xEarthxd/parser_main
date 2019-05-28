#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def nationejobs_parser(file_name):
    
    ### functions
    
    def get_date(soup):
        date_raw = soup.find('th', class_='qualification_postdate align_right').text.split(' ')
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
        title_th = soup.find('th', class_='qualification_positionname align_left').find('a').text.strip()
        return title_th
    
    def get_description(soup):
        description = soup.find('th', class_='qualification_positionname align_left').parent.next_sibling.next_sibling.text.strip().replace('\n', '').replace('\r', '').replace('\t', '')
        return description
    
    def get_education(soup):
        education = {'degree':'', 'major':'', 'faculty':''}
        return education
    
    def get_company(soup):
        company = soup.find('table', class_='table_qualification').find('tr', class_='header').text.strip()
        return company
    
    def get_amount(amount):
        try:
            amount = list(soup.find('th', class_='qualification_positionname align_left'))[1].strip().replace('(', '').replace(')', '')
        except IndexError:
            amount = '1 อัตรา'
        return amount
    
    ### parsing starts here
    
    with open(file_name, 'r', encoding = 'utf-8') as fin:
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
        company = get_company(soup)
    except:
        company = 'Not Found'
        
    try: 
        amount = get_amount(soup)
    except: 
        amount = 'Not Found'
    
    job_parsed = {
        "file_name" : file_name,
        "date": date,
        "title_en": '',
        "title_th": title_th,
        "description": description,
        "qualification": '',
        "education": education,
        "location": '',
        "company": company,
        "amount": amount,
        "exp": '',
        "gender": '',
        "salary": ''
    }
        
    return job_parsed

