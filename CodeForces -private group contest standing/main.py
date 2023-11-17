from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from random import randint as rand
import openpyxl

# Replace these with your Codeforces credentials
username = "Mohab"
password = "mohabashraf123456789"
groupId = "V2UavMqsbA"
contestId = "484385"
#
driver = webdriver.Chrome()
driver.get("https://codeforces.com/enter")
username_input = driver.find_element(By.ID, "handleOrEmail")
password_input = driver.find_element(By.ID, "password")
remember = driver.find_element(By.ID, "remember")
submit_button = driver.find_element(By.CLASS_NAME, "submit")
username_input.send_keys(username)
password_input.send_keys(password)
sleep(1)
submit_button.click()
sleep(3)
driver.get(f"https://codeforces.com/group/{groupId}/contest/{contestId}/standings/groupmates/true")
sleep(2)
users = driver.find_element(By.CLASS_NAME, "standings").find_elements(By.TAG_NAME, "tr")
contestants = []
print(len(users), users)
for i in range(1, len(users) - 1):
    user = users[i].find_elements(By.TAG_NAME, "td")
    user_rank = user[0].text
    user_name = user[1].find_element(By.CLASS_NAME, "rated-user").text
    problems = []
    for ii in range(4, len(user)):
        problem = user[ii]
        try:
            isRejected = problem.find_element(By.CLASS_NAME, "cell-rejected")
            problems.append(isRejected.text if isRejected.text != ' ' else 0)
        except:
            problems.append(problem.find_element(By.CLASS_NAME, "cell-accepted").text)
    user_rank = user_rank if user_rank != ' ' else "*"
    contestants.append([user_rank, user_name, problems])
numOfProblems = len(contestants[0][2])
header = ["Rank", "User"]
for i in range(numOfProblems):
    header.append(chr(i + ord('A')))
print(header)
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(header)

for contestant in contestants:
    li = [contestant[0], contestant[1]]
    for problem in contestant[2]:
        li.append(problem)
    sheet.append(li)
workbook.save(f"contest-{contestId}.xlsx")
driver.quit()
