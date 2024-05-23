This project involves web scraping data from the National Medical Commission (NMC) website to extract information about medical colleges and courses. The project utilizes several Python libraries to automate the browsing process, interact with web elements, and process the extracted data.

Libraries Used

Selenium: For automating web browser interactions.

webdriver: To control the browser.
webdriver.chrome.service.Service: To manage ChromeDriver service.
webdriver.common.by.By: For locating elements.
webdriver.support.ui.WebDriverWait: For waiting until a condition is met.
webdriver.support.expected_conditions as EC: To define conditions for WebDriverWait.
webdriver.support.ui.Select: To handle dropdown menu selections.
Pandas: For data manipulation and analysis.

pd.read_html(): To read HTML tables into DataFrames.
pd.concat(): To concatenate DataFrames.
Webdriver Manager: For automatic management of ChromeDriver.

webdriver_manager.chrome.ChromeDriverManager: To install and manage ChromeDriver.
Time: For adding delays in the script.

Key Functions and Workflow

Setup and Initialization:

The script begins by setting up the Chrome WebDriver using webdriver.Chrome() and configuring it to delete all cookies and set an implicit wait time.
The script navigates to the NMC website and maximizes the browser window.
Interacting with Web Elements:

The course and state dropdown menus are located using their element IDs and are interacted with using the Select class from selenium.webdriver.support.ui.
The script selects "All PG Courses" for the course dropdown and "ALL" for the state dropdown.
Triggering Search and Extracting Data:

The search is triggered by clicking the search button identified by its element ID.
The script waits for the results to load and then extracts the HTML content of the results table using driver.find_element().get_attribute('outerHTML').
Handling Multiple Pages:

The total count of results is checked, and if it exceeds 500, the script handles pagination by clicking the 'Next' button and concatenating the data from multiple pages using pd.concat().
Data Processing:

The final concatenated DataFrame is cleaned by dropping unnecessary columns before further analysis or storage.
Example Code Snippet

python
Copy code
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.delete_all_cookies()
driver.implicitly_wait(10)
driver.get("https://www.nmc.org.in/information-desk/college-and-course-search/")
driver.maximize_window()

# Select course and state
time.sleep(2)
course_name = driver.find_element(By.ID, "list_courses")
select_course = Select(course_name)
select_course.select_by_visible_text("All PG Courses")

state_name = driver.find_element(By.ID, "list_states")
select_state = Select(state_name)
select_state.select_by_visible_text("ALL")

# Trigger search
view_result = driver.find_element(By.ID, "searchCollege")
view_result.click()
time.sleep(5)

# Extract data
data = pd.read_html(driver.find_element(By.ID, "courses").get_attribute('outerHTML'))[0]

# Handle pagination if necessary
Total_count = driver.find_element(By.ID, "totalCount").text
if int(Total_count) > 500:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'courses_next')))
    element.click()
    data_2 = pd.read_html(driver.find_element(By.ID, "courses").get_attribute('outerHTML'))[0]
    merged_data = pd.concat([data, data_2], axis=0, ignore_index=True)

# Process data
final_data = merged_data.drop(['Year of Inception of College', 'Date of LOP', 'Status of MCI/NMC Recognition'], axis=1)
This project demonstrates web scraping skills, handling dynamic web content, and data manipulation using Python, making it a valuable addition to your portfolio. ​​
