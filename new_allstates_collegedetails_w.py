#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:55:12 2024

@author: swetha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:41:12 2024

@author: swetha
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_college_data():
    col_name, links, ph, mail, add, cont = [], [], [], [], [], []
    all_data = pd.DataFrame(columns=["College Name", "Website Link", "Phone Number", "Email ID", "Address", "Contact"])

    while True:
        college_links = driver.find_elements(By.XPATH, "//td/a[contains(@onclick, 'populateCollegeData')]")
        
        for link in college_links:
            try:
                college_name = link.text
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link)).click()
                time.sleep(2)

                clg_name = driver.find_element(By.XPATH, "//*[@class= 'table table-bordered collegeModal']/tbody/tr[1]/td[2]").text
                ph_num = driver.find_element(By.XPATH, "//*[@class= 'table table-bordered collegeModal']/tbody/tr[3]/td[2]").text
                email = driver.find_element(By.XPATH, "//*[@class= 'table table-bordered collegeModal']/tbody/tr[3]/td[6]").text
                address = driver.find_element(By.XPATH, "//*[@class= 'table table-bordered collegeModal']/tbody/tr[4]/td[2]").text
                contact = driver.find_element(By.XPATH, "//*[@class= 'table table-bordered collegeModal']/tbody/tr[5]/td[2]").text
                elem = driver.find_elements(By.XPATH, "//*[@class= 'table table-bordered collegeModal']/tbody/tr[1]/td[2]/a")
                web_site = elem[0].get_attribute("href") if elem else 'N/A'
                
                col_name.append(clg_name)
                links.append(web_site)
                ph.append(ph_num)
                mail.append(email)
                add.append(address)
                cont.append(contact)

                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close')]"))
                )
                close_button.click()
                time.sleep(2)

            except (NoSuchElementException, ElementClickInterceptedException, TimeoutException, StaleElementReferenceException) as e:
                print(f'Error: {e} in {college_name}')
                continue

        # Check if the 'Next' button is present and clickable
        try:
            next_button = driver.find_element(By.ID, "courses_next")
            if "disabled" in next_button.get_attribute("class"):
                print("Next is disabled")
                break  # Exit loop if 'Next' button is disabled
            else:
                print("Next is enabled")
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
        except NoSuchElementException:
            print("Next button not found, breaking loop")
            break  # Exit loop if 'Next' button is not found

    all_data['College Name'] = col_name
    all_data['Website Link'] = links
    all_data['Phone Number'] = ph
    all_data['Email ID'] = mail
    all_data['Address'] = add
    all_data['Contact'] = cont
    
    return all_data

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get("https://www.nmc.org.in/information-desk/college-and-course-search/")
driver.maximize_window()

select_state = Select(driver.find_element(By.ID, "list_states"))
list_states = [opt.text for opt in select_state.options][1:]  # Skip the first option (e.g., "Select State")

for state in list_states:
    # Select course
    time.sleep(2)
    select_course = Select(driver.find_element(By.ID, "list_courses"))
    select_course.select_by_visible_text("ALL MD")

    print(f"Processing state: {state}")

    # Reinitialize the state selection element
    select_state = Select(driver.find_element(By.ID, "list_states"))
    select_state.select_by_visible_text(state)
    
    # Trigger search
    driver.find_element(By.ID, "searchCollege").click()
    time.sleep(5)
    
    state_data = scrape_college_data()
    
    file_path = f"/Users/swetha/Documents/Work/All_MD_collegedetails/{state}_All_MD_college_details.xlsx"
    state_data.to_excel(file_path, index=False)
    print(f"Saved data for {state} to {file_path}")
    driver.refresh()
    time.sleep(5)  # Give some time for the page to refresh properly

driver.quit()
