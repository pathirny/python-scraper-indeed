from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import csv
# set job title and location
start = time.time()
job = "Junior+Software+Engineer"
location = "London"
## data I want to collect
salary = []
job_description = []
job_list = []
url = f"https://uk.indeed.com/m/jobs?q={job}&radius=25&filter=0&l={location}"

# run in Incognito mode
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
# look at the page 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
driver.get(url)
fields = ["Job Title", "URL", "ID", "Company Name", "Location"]
# set the link
# # get the amount of jobs for the search
amount_of_jobs = driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text
# # get amount of jobs per page to iterate over pages
max_pages = int(amount_of_jobs.split(' ')[0])//15
for i in range(max_pages):
    driver.get(f"{url}&start={i * 15}")
    time.sleep(random.randint(2, 4))

    job_page = driver.find_element(By.ID, "mosaic-jobResults")
    jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")
    print(job_page)
    for j in jobs:
        
        job_title = j.find_element(By.CLASS_NAME, "jobTitle") 
        company_name = j.find_element(By.XPATH, "//span[@data-testid='company-name']").text
        company_location = j.find_element(By.XPATH, "//div[@data-testid='text-location']").text

        job_list.append([job_title.text, job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("href"), 
                        job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("id"),
                        company_name,
                        company_location
                        ])
        

driver.quit()

end = time.time()
print(end - start, "seconds to complete search")
print("-------------------")
print("Amount of jobs: ", amount_of_jobs)
print("Max amount of pages for this search: ", max_pages)
print(job_list)

with open('jobs.csv', 'w', newline='') as csvfile:
    jobwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    jobwriter.writerow(fields)
    jobwriter.writerows(job_list)