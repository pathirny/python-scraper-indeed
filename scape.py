from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
# set job title and location
start = time.time()
sleep = time.sleep(random.randint(2,6))
job_title = "Junior+Software+Engineer"
location = "London"
# run in Incognito mode
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
# set the link
url = f"https://uk.indeed.com/m/jobs?q={job_title}&radius=25&filter=0&l={location}"
# look at the page 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
driver.get(url.format(job_title, location,0))
# get the amount of jobs for the search
amount_of_jobs = driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text;
# get amount of jobs per page to iterate over pages
max_pages = int(amount_of_jobs.split(' ')[0])//15
driver.quit()
end = time.time()
print(end - start, "seconds to complete search")
print("-------------------")
print("Amount of jobs: ", amount_of_jobs)
print("Max amount of pages for this search: ", max_pages)