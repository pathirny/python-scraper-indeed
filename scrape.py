from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import csv
from flask import Flask, jsonify
import json
from flask_cors import CORS, cross_origin
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
option.add_argument("start-maximized")
# look at the page 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
driver.get(url)
fields = ["job_title", "URL", "ID", "Company_Name", "Location", "Salary"]
# set the link
# # get the amount of jobs for the search
amount_of_jobs = driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text
 # # get amount of jobs per page to iterate over pages
max_pages = int(amount_of_jobs.split(' ')[0])//15
for i in range(max_pages):
    driver.get(f"{url}&start={i * 15}")
    time.sleep(random.randint(2, 4))
    # have to verify that program is human

    job_page = driver.find_element(By.ID, "mosaic-jobResults")
    jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")
    #print(job_page)
    for j in jobs:
        try:
            job_title = j.find_element(By.CLASS_NAME, "jobTitle") 
        except NoSuchElementException:
            job_title = "None"
        
        try:
            company_name = j.find_element(By.XPATH, "//span[@data-testid='company-name']").text
        except NoSuchElementException:
            company_name = "None"
        company_location = j.find_element(By.XPATH, "//div[@data-testid='text-location']").text

        job_list.append([job_title.text,
                        job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("href"), 
                        job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("id"),
                        company_name,
                        company_location,
                        ])
        
        try:
            salary.append(j.find_element(By.CLASS_NAME, "salary-snippet-container").text)
        except NoSuchElementException:
            try:
                salary.append(j.find_element(By.CLASS_NAME, "estimated-salary").text)
            except NoSuchElementException:
                salary.append("None")
driver.quit()

end = time.time()
print(end - start, "seconds to complete search")
print("-------------------")
print("Amount of jobs: ", amount_of_jobs)
print("Max amount of pages for this search: ", max_pages)
#print(job_list)

# convert the 2 list (fields and job_list) into dictionary
result = []

#dummy_list = [["job1", "url1", "id1", "companyName1", "location1"], ["job2", "url2", "id2", "companyName2", "location2"]]

# for list in dummy_list:
#     for item in list:
#         attempt_list.append(item)

# print(attempt_list)

# print(job_list)

# jobListCopied = [['Software Engineer - Modelling and Simulation', 'https://uk.indeed.com/pagead/clk?mo=r&ad=-6NYlbfkN0AoucB_G_SJpE8RPm3FmLy-hUK9s8ytG_pFzAFTGy7o3pcbijiII1urEfGnHiHUKFT1FvtnInOWYu0_fk87zYAD-5siKYekeyh-YnZk3TN77_AC_2ppjr4wzjxDDRZqCIpZV0bTMdnAovaHkIi2hZwpVj9BoDmDFeNrwZDKOaUVcYzJOXckqtq9_SRNsJwG3ie16VxJYFWEO65IZwNKT1_9tcHXWKp5Fvf9ZwV1Vd559AhMdcZs_m8PEIIYISl5JQjcKytgBrpfL8Q1phkaZ5By4YZeDrpcyzdlwbMO3v_N9cOF17p52liDwiLGHwFAQc5kCG5e7vD_Q6sFE1rwge_FIgTtIZdcmiyNvj3GpC6qz9GOLeULrEK_Dc5wmcfLlEQUd45A8W9jGjsoXWlzMVQRFsn1jfSubIdBhfmshza2cTu3wjPtCuoeki7BfSI1BCVy6Uily3LAhN_v-6o4ttI71L65vzbW_2k9A15OpMZsL9hqQbFi01RWobQRXAUf_YoVB6KyOoNCWjqBz6-JhNEVgqrH4t3OBWFzhos0Hvz2cF6pkDdVUeMMmRAv-wEgE3Rpj0Z1ekY-sG2ezyzK5KGTtsTS8Pi5tIxMLd7R8IFIrTfqhfTzgHdoFkY05N_6u2qjE4Yrukwi9P8KGgt6eHPVLDhQzwilT0qSJNrTSxwHtt-7pTIDl-pZGIzufKoGKROspyWVF9-cCiyavi5gWi4kdPiaJB6vEJOeWt2OkctzhIe7wquaN6LSaQOiM84iMciu1skb17rubN3zMJlVPZG9RylkLrdKnMBH9_q6ofuRFk6ByWzLwFSMOqrAjy2qcM8q3cqfB9lj9Q==&xkcb=SoA86_M3D471YIgI_r0LbzkdCdPP&camk=4HOcmqOLYrBhPnBb-cy5xQ==&p=0&fvj=0&vjs=3', 'sj_6f2091c334c10398', 'Northrop Grumman', 'Hybrid remote in London'], ['Lead Core Java Developer', 'https://uk.indeed.com/rc/clk?jk=e4195132078cf1b5&bb=fD2PxZfr3Bv_NyrO_71u-Z5MSgFTQWRKyuJem0oARmDkWElt-5a7N5jPrEWgMvzy5MxxQnWb9FddzfZjNLXfhwzuQR-SwmCknwSCcybqzYuNX8fobSSsWw%3D%3D&xkcb=SoAo67M3D47wNrAI_L0GbzkdCdPP&fccid=9353252f275fbb30&vjs=3', 'job_e4195132078cf1b5', 'Warner Bros. Discovery', 'London W4'], ['Principal Python Engineer - Core (Remote)', 'https://uk.indeed.com/rc/clk?jk=3cd4223b21688df5&bb=fD2PxZfr3Bv_NyrO_71u-WlPVLwfgc4OilCZb_FsP-tu0uCZNecWgFUK4uANuy1NICO222ptUTMutaaP080fHxuEhxqI6d-tYnjPTScIQNWvRRdJoEiRPg%3D%3D&xkcb=SoC167M3D47wNrAI_L0FbzkdCdPP&fccid=93143575209a3ce4&vjs=3', 'job_3cd4223b21688df5', 'Warner Bros. Discovery', 'London W4']]
#     #print(key)

for job, sal in zip(job_list, salary):
    job_dict = dict(zip(fields, job))
    job_dict['salary'] = sal
    result.append(job_dict)

json_result = json.dumps(result)
########## each job return a array which contains all the info in an array, will need another for loop to iterate over each element?
print(result)
# # find a way to get fields in Columns and rows as the scraped information

field_names = list(job_dict.keys())
with open('jobs.csv', 'w', newline='') as csvfile:
    jobwriter = csv.DictWriter(csvfile, fieldnames=field_names)
    jobwriter.writeheader()
    
    for job in result:
        jobwriter.writerow(job)

# create api to visualise the data
#print(result)
     
app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def indeedData():
    return json_result

if __name__ == '__main__':
    app.run(port=5000)