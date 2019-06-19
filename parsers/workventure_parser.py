#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import os
import datetime
import json
import io


# In[ ]:


def workventure_parser(file_name):
    
    ### functions
    
    def get_date(data):
        if data.get('data').get('attributes').get('created_at') is not None:
            date_raw = data.get('data').get('attributes').get('created_at').split(' ')[0]
            date = datetime.datetime(year = int(date_raw.split('-')[0]), month = int(date_raw.split('-')[1]), day = int(date_raw.split('-')[2]))
        if data.get('data').get('attributes').get('created_at') is None:
            for item in data.get('included'):
                if item['type'] == 'company':
                    date_raw = item['attributes']['updated_at']['date'].split(' ')[0]
                    date = datetime.datetime(year = int(date_raw.split('-')[0]), month = int(date_raw.split('-')[1]), day = int(date_raw.split('-')[2]))
        return date
    
    def get_title_en(data):
        title_en = data.get('data').get('attributes').get('position')
        return title_en
    
    def get_title_th(data):
        title_th = data.get('data').get('attributes').get('position_th')
        return title_th
    
    def get_description(data):
        description = ''
        for item in data.get('data').get('attributes').get('responsibilities'):
            description += item + ' / '
        return description
    
    def get_qualification(data):
        qualification = ''
        for item in data.get('data').get('attributes').get('qualifications'):
            qualification += item + ' / '
        return qualification
    
    def get_education(data):
        for item in data.get('included'):
            education = [{'degree': '', 'faculty': '', 'major': ''}]
            if item['type'] == 'educations':
                education[0]['degree'] = ''
                education[0]['major'] = ''
                education[0]['faculty'] = item['attributes']['name']
            elif (item['type'] == 'educations') is None: 
                education = [{'degree': '', 'faculty': '', 'major': ''}]
        return education

    def get_location(data):
        for item in data.get('included'):
            if item['type'] == 'company':
                location = item['attributes']['location']['address']
        return location
    
    def get_company(data):
        for item in data.get('included'):
            if item['type'] == 'company':
                company = item['attributes']['name']
        return company
    
    def get_amount(data):
        for item in data.get('included'):
            if item['type'] == 'company':
                company = str(item['attributes']['jobs_count'])
        return company
    
    def get_exp(data):
        for item in data.get('included'):
            if item['type'] == 'experienceRequired':
                exp = item['attributes']['name']
        return exp
    
    def get_salary(data):
        if (data.get('data').get('attributes').get('salary')['min'] and data.get('data').get('attributes').get('salary')['max']) is None:
            salary = 'Negotiable'
        if (data.get('data').get('attributes').get('salary')['min'] and data.get('data').get('attributes').get('salary')['max']) is not None:
            salary = data.get('data').get('attributes').get('salary')['min'] + ' - ' + data.get('data').get('attributes').get('salary')['max']
        return salary
    
    def get_gender(data):
        if (data.get('data').get('attributes').get('can_apply')['male'] and data.get('data').get('attributes').get('can_apply')['female']) > 0:
            gender = 'male / female'
        if (data.get('data').get('attributes').get('can_apply')['male'] > 0) and (data.get('data').get('attributes').get('can_apply')['female'] == 0):
            gender = 'male'
        if (data.get('data').get('attributes').get('can_apply')['male'] == 0) and (data.get('data').get('attributes').get('can_apply')['female'] < 0):
            gender = 'female'
        return gender
        
    def get_functions(data):
        functions = []
        for item in data.get('included'):
            if item['type'] == 'functions':
                functions.append(item['attributes']['name'])
        return functions
    
    def get_skillCategory(data):
        skill_category = []
        for item in data.get('included'):
            if item['type'] == 'skillCategory':
                skill_category.append(item['attributes']['name'])
        return skill_category
        
    def get_skillPreferred(data):
        skill_preferred = []
        for item in data.get('included'):
            dict_skill = {}
            if item['type'] == 'skillsPreferred':
                dict_skill['name'] = item['attributes']['name']
                dict_skill['level'] = item['attributes']['level']
                skill_preferred.append(dict_skill)            
        return skill_preferred
    
    ### parsing starts here
    
    with open(file_name, 'rb') as fin:
        data = json.loads(fin.read())
        
    try:
        date = get_date(data)
    except:
        date = 'Not Found'
    
    try:
        title_en = get_title_en(data)
    except:
        title_en = 'Not Found'
    
    try:
        title_th = get_title_th(data)
    except:
        title_th = 'Not Found'
        
    try:
        description = get_description(data)
    except:
        description = 'Not Found'
    
    try:
        qualification = get_qualification(data)
    except:
        qualification = 'Not Found'
    
    try: 
        education = get_education(data)
    except:
        education = 'Not Found'
    
    try:
        location = get_location(data)
    except:
        location = 'Not Found'
        
    try:
        company = get_company(data)
    except:
        company = 'Not Found'
        
    try: 
        amount = get_amount(data)
    except: 
        amount = 'Not Found'
    
    try:
        exp = get_exp(data)
    except:
        exp = 'Not Found'
    
    try:
        gender = get_gender(data)
    except:
        gender = 'Not Found'
        
    try:
        salary = get_salary(data)
    except:
        salary = 'Not Found'
    
    try:
        functions = get_functions(data)
    except:
        functions = 'Not Found'
    
    try:
        skill_category = get_skillCategory(data)
    except:
        skill_category = 'Not Found'
        
    try:
        skill_preferred = get_skillPreferred(data)
    except:
        skill_preferred = 'Not Found'
    
    job_parsed = {
        "file_name" : file_name,
        "date": date,
        "title_en": title_en,
        "title_th": title_th,
        "description": description,
        "qualification": qualification,
        "education": education,
        "location": location,
        "company": company,
        "amount": amount,
        "exp": exp,
        "gender": gender,
        "salary": salary,
        "functions" : functions,
        "skill_category" : skill_category,
        "skill_preferred" : skill_preferred
    }
    
    return job_parsed

