# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 12:05:47 2022

@author: amana
"""

import pandas as pd

import glassdoor_scrapper as gs

path = 'C:/Users/amana/OneDrive/Desktop/glassdoor_salary_analysis/chromedriver'

df = gs.get_jobs("Data Science",5,False,20)


