#!/usr/bin/env python
# coding: utf-8

# In[21]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobsawasdee_parser(file_name):
    
    ### functions
    
    def get_date(soup):
        date_raw = soup.find_all('div', class_='text-blue')[0].get_text().split(' ')
        month_real = ''
        month_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_th = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
        for month in month_th:
            num = month_th.index(month)
            if date_raw[3] == month:
                month_real = month_num[num]
        
        year = int(soup.find_all('div', class_='text-blue')[0].get_text().split(' ')[4])  + 1957
        date = datetime.datetime(year = int(year), month = int(month_real), day = int(date_raw[2]))
        return date
    
    def get_title(soup):
        title_th = soup.find('span', class_='text_BB').get_text().split(':')[0].replace('\xa0', '')
        return title_th
    
    def get_description(soup):
        description = soup.find('td', width='489').get_text().replace('\r', '').replace('\n', '').replace('\t', '')
        return description
    
    def get_education(soup):
        education = []
        edu_dict = {}
        edu_dict['degree'] = soup.find('strong', text='คุณสมบัติผู้สมัคร').parent.parent.next_sibling.next_sibling.get_text().strip().replace('\n', '').replace('\xa0','').replace('\r','').replace('        ',' ')
        edu_dict['major'] = ''
        edu_dict['faculty'] = ''
        education.append(edu_dict)
        return education
    
    def get_qualification(soup):
        for item in soup.find_all('td', valign='top'):
            counters = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10,.']
            for counter in counters:
                if not counter in item.text:continue
                qualification = qualification + item.next_sibling.next_sibling.get_text().strip() + '/'
        return qualification
    
    def get_exp(soup):
        for item in soup.find_all('td', class_='dot'):
            if not 'ประสบการณ์' in item.text:continue
            exp = item.text.strip().replace('\r','').replace('\n','').replace('        ', ' ')
        return exp
    
    def get_amount(soup):
        amount = soup.find('span', class_='text_BB').get_text().split(':')[1].strip().replace('        ', ' ')
        return amount
    
    def get_gender(soup):
        gender = soup.find('strong', text='คุณสมบัติผู้สมัคร').parent.next_sibling.next_sibling.get_text().split(' ')[0]
        return gender
    
    def get_location(soup):
        location = soup.find('strong', text="ที่อยู่").parent.next_sibling.next_sibling.get_text().strip() + ' ' + soup.find('strong', text = "จังหวัด").parent.next_sibling.next_sibling.text.strip()
        return location
    
    def get_company(soup):
        company = soup.find_all('strong', class_="text_BB")[0].get_text().strip()
        return company
    
    def get_salary(soup):
        salary = soup.find('strong', text="เงินเดือน").parent.next_sibling.next_sibling.get_text().strip().replace('\xa0', '')
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
    

