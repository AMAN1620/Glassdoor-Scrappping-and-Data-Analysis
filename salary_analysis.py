# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 23:54:02 2022

@author: amana
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')

data = pd.DataFrame(df)

# salary parsing 
data = data[data['Salary Estimate'] != '-1']
data_temp = data

data_temp.drop('Unnamed: 0',axis = 1,inplace=True)
data_temp['hourly '] = data_temp['Salary Estimate'].apply(lambda x : 1 if 'per hour' in x.lower() else 0)
data_temp['Employer Provided Salary'] = data_temp['Salary Estimate'].apply(lambda x : 1 if 'employer provided' in x.lower() else 0)

salary = data['Salary Estimate'].apply(lambda x: x.split('(')[0])

salary = salary.apply(lambda x: x.lower().replace('employer provided salary:','').replace('per hour',''))

salary = salary.apply(lambda x : x.replace('$','').replace('k',''))

# finding the min and max & avg salary from the salary estimates
data_temp['min_salary(in k)'] = salary.apply(lambda x:int(x.split('-')[0]))
data_temp['max_salary(in k)'] = salary.apply(lambda x:int(x.split('-')[1]))
data_temp['average_salary'] = (data_temp['min_salary(in k)'] +data_temp['max_salary(in k)'])/2

# company name text only
data_temp['Company_name'] = data_temp.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis = 1)

# state field
data_temp['job_state'] = data_temp['Location'].apply(lambda x:x.split(',')[1])
data_temp['same_state'] = data_temp.apply(lambda x: 1 if (x['Location']==x['Headquarters']) else 0,axis = 1)


# age of the company
data_temp['Founded'].dtype
data_temp['age'] = data_temp.apply(lambda x: 0 if x['Founded']<0 else (2022-x['Founded']),axis = 1)

# Type of Ownership
print(data_temp['Type of ownership'].value_counts())
data_temp['ownership'] = data_temp.apply(lambda x: 1 if 'Private' in x['Type of ownership'] else 0,axis = 1)

# parsing some info from description
# Python in job desc
data_temp['python'] = data_temp['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
print(data_temp.python.value_counts())

# MATLAB in job desc
data_temp['matlab'] = data_temp['Job Description'].apply(lambda x: 1 if 'matlab' in x.lower() else 0)
print(data_temp.matlab.value_counts())

# Cloud in job desc
data_temp['cloud'] = data_temp['Job Description'].apply(lambda x: 1 if 'cloud' in x.lower() else 0)
print(data_temp.cloud.value_counts())

# sql in job desc
data_temp['sql'] = data_temp['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
print(data_temp.sql.value_counts())

# Excel in job desc
data_temp['excel'] = data_temp['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
print(data_temp.excel.value_counts())

data_temp.to_csv('jobs_cleaned_data.csv',index=False)

cleaned = pd.read_csv('jobs_cleaned_data.csv')
print(cleaned.head())
