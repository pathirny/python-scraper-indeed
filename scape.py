from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
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
        

        job_list.append([job_title.text, job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("href"), 
                        job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("id"),
                        j.find_element(By.CSS_SELECTOR, "span[data-testid='companyName']").text,
                        j.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']").text,
                        j.find_element(By.CLASS_NAME, "date").text,
                        job_title.find_element(By.CLASS_NAME, "a").get_attribute("href")])
        

driver.quit()

end = time.time()
print(end - start, "seconds to complete search")
print("-------------------")
print("Amount of jobs: ", amount_of_jobs)
print("Max amount of pages for this search: ", max_pages)
print(job_list)
