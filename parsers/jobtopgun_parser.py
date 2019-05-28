#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[ ]:


def jobtopgun_parser(file_name):
    
    ### functions
    
    # Convert B.C. into A.D. and datetime standard
    def get_date(soup):
        date_raw = soup.find('div', attrs={"clas": "dateAndShare"}).find('p').get_text().strip()
        date_raw = date_raw.split('/')
        date = datetime.datetime(year = int(date_raw[2]) - 543, month = int(date_raw[1]), day = int(date_raw[0]))
        return date
    
    def get_title(soup):
        title_th = soup.find("div", class_="font_22_bold").get_text().strip()
        return title_th
    
    def get_description(soup):
        if soup.find("div", class_="jobDescription") is None:
            description = ''
            return description
        else:
            description = soup.find("div", class_="jobDescription").find("table").find("tr").find("td").get_text().strip().replace('\n','').replace('\t','').replace('   ',' ').replace('  ',' ').replace(u'\xa0', u' ').replace('\r','')
            return description
    
    def get_qualification(soup):
        if soup.find("div", id="qualification") is None:
            qualification = ''
            return qualification
        else:
            qualification = soup.find("div", id="qualification").find("table").find("tr").find("td").get_text().strip().replace('\n','').replace('\t','').replace('   ',' ').replace('  ',' ').replace(u'\xa0', u' ').replace('\r','')
            return qualification
    
    # Get list of Education in {[degree: '', faculty: '', major: '']} format
    def add_edu(faculties, degree):
        education = []
        
        if str(soup.find_all('span', text="คณะ : ")) != '[]':
            for faculty in faculties:
                edu_dict = {}
                edu_dict['degree'] = degree

                if faculty.next_sibling.next_sibling.next_sibling is None :
                    edu_dict['major'] = ''
                elif 'สาขา : ' in faculty.next_sibling.next_sibling.next_sibling :
                    edu_dict['major'] = faculty.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
                elif faculty.next_sibling.next_sibling.next_sibling is not str :
                    edu_dict['major'] = ''
                else :
                    edu_dict['major'] = ''

                edu_dict['faculty'] = faculty.next_sibling.get_text()
                education.append(edu_dict)
        
        # Case : Only contain educational field, no faculty / major fields.
        elif str(soup.find_all('span', text="คณะ : ")) == '[]':
            edu_dict = {}
            edu_dict['degree'] = degree
            edu_dict['major'] = ''
            edu_dict['faculty'] = ''
            education.append(edu_dict)

        return education
    
    def get_location(soup):
        location = list(soup.find('span', text = "สถานที่ : ").next_siblings)[1].get_text().strip()
        return location
    
    def get_amount(soup):
        amount = list(soup.find('span', text = "จำนวน : ").next_siblings)[1].get_text().strip()
        return amount
    
    def get_exp(soup):
        exp = list(soup.find('span', text = "ประสบการณ์ : ").next_siblings)[1].get_text().replace('\n','').replace('\t','').replace(' ','').replace('\r', '')
        return exp
    
    def get_gender(soup):
        gender = soup.find('span', text = "เพศ : ").next_sibling.get_text()
        return gender
    
    def get_salary(soup):
        salary = list(soup.find('span', text = "เงินเดือน(บาท) : ").next_siblings)[1].get_text().strip().replace('\n','').replace('\t','').replace('   ',' ').replace('  ',' ').replace(u'\xa0', u' ').replace('\r','')
        return salary
    
    def get_company(soup):
        company = soup.find('div', class_="companyName").get_text().strip()
        return company
    
    ### parsing starts here
    
    with open(file_name, 'rb') as fin:
        soup = BeautifulSoup(fin.read(), features = "html.parser")
    
    faculties = soup.find_all('span', text="คณะ : ")
    
    # Case : Some jobads didn't provide class 'jobPostFacultyLabel' which returning None as the result.
    if soup.find("span", class_="jobPostFacultyLabel") is None:
        degree = soup.find('span', text = 'การศึกษา : ').next_sibling.next_sibling.get_text().strip()
    else:
        degree = soup.find("span", class_="jobPostFacultyLabel").previous_sibling.previous_sibling.previous_sibling.strip()
    
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
        education = add_edu(faculties, degree)
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
        "title_en": "",
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

