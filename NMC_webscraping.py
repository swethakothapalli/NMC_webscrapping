#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:30:27 2024

@author: swetha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:30:25 2024

@author: swetha
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.delete_all_cookies()
driver.implicitly_wait(10)

driver.get("https://www.nmc.org.in/information-desk/college-and-course-search/")
driver.maximize_window()


time.sleep(2)

course_name = \
driver.find_element(By.ID, "list_courses")
select_course = Select(course_name)
# select_course.select_by_visible_text("M.B.B.S.")
select_course.select_by_visible_text("All PG Courses") # give the visible text here


state_name = \
driver.find_element(By.ID, "list_states")
select_state = Select(state_name)

select_state.select_by_visible_text("ALL")

view_result = driver.find_element(By.ID, "searchCollege")
view_result.click()
  
time.sleep(5)

    
data = pd.read_html(driver.find_element(By.ID, "courses").get_attribute('outerHTML'))[0]



driver.implicitly_wait(10)

Total_count = driver.find_element(By.ID, "totalCount").text
#
if (int (Total_count)> 500):
    print(driver.find_element(By.ID, "totalCount").text)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'courses_next')))
    element.click()
    data_2 = pd.read_html(driver.find_element(By.ID, "courses").get_attribute('outerHTML'))[0]
    merged_data = df_combined = pd.concat([data, data_2], axis=0, ignore_index=True)

final_data = merged_data.drop(['Year of Inception of College', 'Date of LOP','Status of MCI/NMC Recognition'], axis=1)   
driver.quit()
final_data = data.drop(['Year of Inception of College', 'Date of LOP','Status of MCI/NMC Recognition'], axis=1)   

final_data.to_excel(r"/Users/swetha/Documents/Work/All_states_coursenames/mbbs_all_states.xlsx", index=False)
# final_data.to_excel(r"/Users/swetha/Documents/Work/All_states_coursenames/pg_allstates.xlsx", index=False)
