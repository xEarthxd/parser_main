#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobthai_parser(file_name):
    
    ### functions
    
    def get_date(soup):
        date_raw = soup.find('span', class_='head1 gray').text.split(' ')
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
        if soup.find('span', class_='head5 blue') is None:
            title_th = ''
        else:
            title_th = soup.find('span', class_='head5 blue').text.strip()
        return title_th

    def get_description(soup):
        if soup.find('span', text='รายละเอียดของงาน') is None:
            description = ''
        else:
            description = soup.find('span', text='รายละเอียดของงาน').parent.parent.next_sibling.next_sibling.text.strip().replace('\n','').replace('\r','').replace('\t','')
        return description

    def get_qualification(soup):
        if soup.find('span', text='คุณสมบัติผู้สมัคร') is None:
            qualification = ''
        else:
            qualification = soup.find('span', text='คุณสมบัติผู้สมัคร').parent.parent.next_sibling.next_sibling.text.strip().replace('\n','').replace('\r','').replace('\t','').replace('\xa0', '')
        return qualification

    def get_education(soup):
        education = [{'degree':'', 'major':'','faculty':''}]
        return education

    def get_company(soup):
        if soup.find('span', class_='head5 orange') is None:
            company = ''
        else:
            company = soup.find('span', class_='head5 orange').text.strip()
        return company

    def get_amount(soup):
        if soup.find('span', text = 'อัตรา') is None:
            amount = ''
        else:
            amount = list(soup.find('span', text = 'อัตรา').parent.parent.next_sibling.next_sibling.children)[1].text
        return amount

    def get_salary(soup):
        try:
            salary = list(soup.find('span', text = 'อัตรา').parent.parent.next_sibling.next_sibling.children)[3].text
        except IndexError:
            salary = ''
        return salary

    def get_location(soup):
        location = soup.find('span', text = 'สถานที่ปฏิบัติงาน').parent.parent.next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n','')
        location2 = salary2 = ' '.join(location.split())
        return location2
    
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

