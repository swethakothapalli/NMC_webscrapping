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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get("https://www.nmc.org.in/information-desk/college-and-course-search/")
driver.maximize_window()

# Select course and state
time.sleep(2)
select_course = Select(driver.find_element(By.ID, "list_courses"))
select_course.select_by_visible_text("All PG Courses")

select_state = Select(driver.find_element(By.ID, "list_states"))
select_state.select_by_visible_text("ALL")

# Trigger search
driver.find_element(By.ID, "searchCollege").click()
time.sleep(5)

# Function to extract table data
def extract_table_data():
    table = driver.find_element(By.ID, "courses")
    return pd.read_html(table.get_attribute('outerHTML'))[0]

# Initialize an empty DataFrame to hold all data
all_data = pd.DataFrame()

while True:
    # Extract data from the current page
    data = extract_table_data()
    all_data = pd.concat([all_data, data], axis=0, ignore_index=True)
    
    # Check if the 'Next' button is present and clickable
    try:
        next_button = driver.find_element(By.ID, "courses_next")
        if "disabled" in next_button.get_attribute("class"):
            break  # Exit loop if 'Next' button is disabled
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    except:
        break  # Exit loop if 'Next' button is not found

# Process final data if needed
final_data = all_data.drop(['Year of Inception of College', 'Date of LOP', 'Status of MCI/NMC Recognition'], axis=1)
final_data.to_excel(r"/Users/swetha/Documents/Work/All_states_coursenames/ALL_PG_all_states.xlsx", index=False)
print(final_data)

# Close the WebDriver
driver.quit()

final_data.to_excel(r"/Users/swetha/Documents/Work/All_states_coursenames/mbbs_all_states.xlsx", index=False)
# final_data.to_excel(r"/Users/swetha/Documents/Work/All_states_coursenames/pg_allstates.xlsx", index=False)
