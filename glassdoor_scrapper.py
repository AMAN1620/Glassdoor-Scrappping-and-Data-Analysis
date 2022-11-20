# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:36:45 2022

@author: amana
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By

def get_jobs(keyword,num_jobs,verbose,slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    #extra line it "solved issue of device attached to system error...."
    options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=r'C:/Users/amana/OneDrive/Desktop/glassdoor_salary_analysis/chromedriver', options=options)
    driver.set_window_size(1120, 1000)

    #url = 'https://www.glassdoor.co.in/Job/india-data-science-jobs-SRCH_IL.0,5_IN115_KO6,18.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=India&context=Jobs&dropdown=0'
    #driver.get(url)
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            # Selected one
            driver.find_element(By.XPATH,'.//*[@id="MainCol"]/div[1]/ul/li[1]').click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.CSS_SELECTOR,'[alt="Close"]').click()  #clicking to the X.
        except NoSuchElementException:
            pass

        
        #Going through each job in this page
        try:
            job_buttons = driver.find_elements(By.XPATH,".//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']") #jl for Job Listing. These are the buttons we're going to click.
            print("Passed 3")
        except NoSuchElementException:
            print("Failed 3")
            pass

        
        for job_button in job_buttons:
            print("Entered for loop")

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click() #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH,"//div[@class='css-87uc0g e1tk4kwz1']").text
                    location = driver.find_element(By.XPATH,"//div[@class='css-56kyx5 e1tk4kwz5']").text
                    job_title = driver.find_element(By.XPATH,"//div[@class='css-1vg6q84 e1tk4kwz4']").text
                    job_description = driver.find_element(By.XPATH,"//div[@id='JobDescriptionContainer']").text
                    collected_successfully = True
                    #print(company_name,location,job_title)
                except:
                    print("fail3")
                    time.sleep(5)
                    break

            try:
                salary_estimate = driver.find_element(By.XPATH,'//span[@class="css-1xe2xww e1wijj242"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
                pass
            
            try:
                rating = driver.find_element(By.XPATH,'//span[@class="css-1m5m32b e1tk4kwz2"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
                pass

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #

            try:
                driver.find_element(By.XPATH,'.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    #

                    #    Headquarters
                    #    San Francisco, CA
                    #

                    headquarters = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_elements(By.XPATH,'.//li[@class="next"]//a')
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
