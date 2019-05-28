#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
from bs4 import BeautifulSoup, Comment


# In[50]:


def jobpub_parser(file_name):

    # Convert B.C. into A.D. and datetime standard
    def get_date(soup):
        return date
    
    def get_title(soup):
        title_th = soup.find('font', face='Arial').get_text()
        return title_th
        
    def get_desctription(soup):
        description = soup.find('font', text='Job Description :').parent.next_sibling.next_sibling.text.replace('\n', '').strip()
        return description
    
    def get_qualification(soup):
        qualification = soup.find('td', style="padding-left: 4; padding-right: 4").text.replace('\br', '').replace('\n', '').strip()
        return qualification
        
    def get_edu(soup):
        education = []
        edu_dict = {}
        edu_dict['degree'] = ''
        edu_dict['major'] = ''
        edu_dict['faculty'] = ''
        education.append(edu_dict)
        return education
    
    def get_location(soup):
        location = soup.find('font', text='Location :').parent.next_sibling.next_sibling.text.replace('\n', '').strip()
        return location
    
    def get_company(soup):
        company = soup.find('span', style="font-family: Arial; font-size: 14pt;").text
        return company
    
    def get_amount(soup):
        amount = soup.find('font', text='Need : ').parent.next_sibling.text.replace('\n', '').strip()
        return amount
    
    def get_exp(soup):
        exp = ''
        return exp
    
    def get_gender(soup):
        gender = ''
        return gender
    
    def get_salary(soup):
        salary = soup.find('font', text='Salary : ').parent.next_sibling.text.replace('\n', '').strip()
        return salary
    
    ### parsing starts here
    
    with open(file_name, 'r', encoding='utf-8') as fin:
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
        qualification = get_qualification(soup)
    except:
        qualification = 'Not Found'
    
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
    "date": '',
    "title_en": '',
    "title_th": title_th,
    "description": description,
    "qualification": qualification,
    "education": education,
    "location": location,
    "company": company,
    "amount": amount,
    "exp": exp,
    "gender": gender ,
    "salary": salary
    }
    
    return job_parsed





