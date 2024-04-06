from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import csv
from flask import Flask, jsonify, Response
import json
from flask_cors import CORS, cross_origin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

fields = ["job_title", "URL", "ID", "Company_Name", "Location", "Salary"]

# set the link
# # get the amount of jobs for the search
amount_of_jobs = driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text

# # get amount of jobs per page to iterate over pages
max_pages = int(amount_of_jobs.split(' ')[0])//15
# this iterates over each page on the search
for i in range(max_pages):
    # this loads the URL and iterates over each page - max_pages 
    driver.get(f"{url}&start={i * max_pages}")
    # time.sleep to give the page time to render all contents
    time.sleep(random.randint(2, 4))
    
    # have to verify that program is human
    # this gets the mosaicResults
    job_page = driver.find_element(By.ID, "mosaic-jobResults")
    jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")
    # iterate over the results (jobs) - iterating over each job 
    for j in jobs:
        try:
            job_title = j.find_element(By.CLASS_NAME, "jobTitle")
            job_link = job_title.find_element(By.TAG_NAME, "a").get_attribute("href")
            job_id = job_title.find_element(By.TAG_NAME, "a").get_attribute("id")
            job_title_text = job_title.text
        except NoSuchElementException:
            job_title_text = "None"
            job_link = "None"
            job_id = "None"
        
        try:
            company_name = j.find_element(By.XPATH, ".//span[@data-testid='company-name']").text
        except NoSuchElementException:
            company_name = "None"
        
        try:
            company_location = j.find_element(By.XPATH, ".//div[@data-testid='text-location']").text
        except NoSuchElementException:
            company_location = "None"
        
        job_list.append([job_title_text, job_link, job_id, company_name, company_location])
        
        try:
            salary_snippet = j.find_element(By.CLASS_NAME, "salary-snippet-container").text
        except NoSuchElementException:
            try:
                salary_snippet = j.find_element(By.CLASS_NAME, "estimated-salary").text
            except NoSuchElementException:
                salary_snippet = "None"
                
        salary.append(salary_snippet)

driver.quit()
end = time.time()

print(end - start, "seconds to complete search")
print("Amount of jobs: ", amount_of_jobs)
print("Max amount of pages for this search: ", max_pages)

result = []

for job, sal in zip(job_list, salary):
    job_dict = dict(zip(fields, job))
    job_dict['Salary'] = sal
    result.append(job_dict)

json_result = json.dumps(result)


field_names = list(fields)
with open('jobs.csv', 'w', newline='') as csvfile:
    jobwriter = csv.DictWriter(csvfile, fieldnames=field_names)
    jobwriter.writeheader()
    
    for job in result:
        jobwriter.writerow(job)

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def indeedData():
    json_result = json.dumps(result)
    return Response(json_result, content_type='application/json')

if __name__ == '__main__':
    app.run(port=5000)
