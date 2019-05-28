#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobthaiweb_parser(file_name):
    
    ### functions
    
    def get_date(soup):
        date_raw = soup.find('b', text='ปรับปรุงข้อมูลเมื่อ').parent.next_sibling.next_sibling.text.split(' ')
        month_real = ''
        month_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_th = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
        for month in month_th:
            num = month_th.index(month)
            if date_raw[1] == month:
                month_real = month_num[num]
        
        year = int(date_raw[2])  - 543
        date = datetime.datetime(year = int(year), month = int(month_real), day = int(date_raw[0]))
        return date
    
    def get_title(soup):
        title_th = soup.find('span', class_='head_topic_white').text.strip()
        return title_th
    
    def get_description(soup):
        description = soup.find('b', text='ลักษณะการทำงาน').parent.next_sibling.next_sibling.text.strip().replace('\r','').replace('\n','').replace('\t','')
        return description
    
    def get_qualification(soup):
        qualification = soup.find('b', text='คุณสมบัติผู้สมัคร').parent.next_sibling.next_sibling.text.strip().replace('\xa0', '').replace('\n', '').replace('\r','').replace('\t','')
        return qualification
    
    def get_education(soup):
        education = [{'degree':'', 'major':'','faculty':''}]
        return education
    
    def get_location(soup):
        if soup.find('b', text = 'เขตพื้นที่ปฏิบัติงาน ') is None:
            location = soup.find('b', text = 'จังหวัดที่ปฏิบัติงาน ').parent.next_sibling.next_sibling.text.strip()
        elif soup.find('b', text = 'จังหวัดที่ปฏิบัติงาน ') is None:
            location = soup.find('b', text = 'เขตพื้นที่ปฏิบัติงาน ').parent.next_sibling.next_sibling.text.strip()
        elif soup.find('b', text = 'เขตพื้นที่ปฏิบัติงาน ') and soup.find('b', text = 'เขตพื้นที่ปฏิบัติงาน ') is None:
            location = ''
        else: 
            location = soup.find('b', text = 'เขตพื้นที่ปฏิบัติงาน ').parent.next_sibling.next_sibling.text.strip() + ' ' + soup.find('b', text = 'จังหวัดที่ปฏิบัติงาน ').parent.next_sibling.next_sibling.text.strip()
            
        return location
    
    def get_company(soup):
        company = soup.find('span', class_='head_topic_black').text.strip()
        return company
    
    def get_amount(soup):
        amount = soup.find('b', text = 'จำนวน ').parent.next_sibling.next_sibling.text.strip()
        return amount
    
    def get_salary(soup):
        salary = soup.find('b', text = 'ระดับเงินเดือน').parent.next_sibling.next_sibling.text.strip()
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
        "exp": '',
        "gender": '',
        "salary": salary
        }
    
    return job_parsed

