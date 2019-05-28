#!/usr/bin/env python
# coding: utf-8

# In[2]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobant_parser(file_name):
    
    ### functions

    def get_date(soup):
        date_raw = soup.find('span', itemprop = "datePosted").get_text()
        date_raw = date_raw.split('/')
        date = datetime.datetime(year = int(date_raw[2]), month = int(date_raw[1]), day = int(date_raw[0]))
        return date
    
    def get_title(soup):
        title_th = soup.find('p', class_='c1').get_text()
        return title_th
        
    def get_desctription(soup):
        description = soup.find('span', text = 'รายละเอียดงาน / คุณสมบัติอื่นๆ / วิธีการรับสมัคร :').parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip().replace('\r','').replace('\t','') 
        return description
        
    def get_edu(soup):
        education = []
        edu_dict = {}
        edu_dict['degree'] = soup.find('span', text = 'การศึกษา : ').parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip()
        edu_dict['major'] = ''
        edu_dict['faculty'] = ''
        education.append(edu_dict)
        return education
    
    def get_location(soup):
        location = soup.find('span', text = ('สถานที่ทำงาน : ')).parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip()
        return location
    
    def get_company(soup):
        company = soup.find('span', itemprop = 'name').get_text()
        return company
    
    def get_amount(soup):
        amount = soup.find('span', text = ('อัตราที่รับ : ')).parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip() 
        return amount
    
    def get_exp(soup):
        exp = soup.find('span', text = ('ประสบการณ์ทำงาน (ปี) : ')).parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip() 
        return exp
    
    def get_gender(soup):
        gender = soup.find('span', text = ('เพศ : ')).parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip()
        return gender
    
    def get_salary(soup):
        salary = soup.find('span', text = ('เงินเดือน : ')).parent.parent.next_sibling.next_sibling.get_text().replace('\n','').strip() 
        return salary
    
    ### parsing starts here
    
    with open(file_name, 'rb') as fin:
        soup = BeautifulSoup(fin.read(), features = "html.parser")
        
    try:
        date = get_date(soup)
    except:
        date = "Not Found"
    
    try:
        title_th = get_title(soup)
    except:
        title_th = "Not Found"
    
    try:
        description = get_desctription(soup)
    except:
        description = 'Not Found'
    
    try: 
        education = get_edu(soup)
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
        "gender": gender ,
        "salary": salary
        }
    
    return job_parsed

