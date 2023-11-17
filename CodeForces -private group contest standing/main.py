from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, time
from random import randint as rand
import openpyxl

# Replace these with your Codeforces credentials
username = "Manger_Handle"
password = "Manger_password"
groupId = "group_id"
contestId = "contest_id"
#
haveHeader = False
start_time = time()
workbook = openpyxl.Workbook()
sheet = workbook.active


def doHeader(tot: int):
    header = ["Rank", "User"]
    for iii in range(tot):
        header.append(chr(iii + ord('A')))
    return header


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

limit = 1
for idx in range(1, limit + 1):
    driver.get(f"https://codeforces.com/group/{groupId}/contest/{contestId}/standings/groupmates/true/page/{idx}")
    sleep(2)
    try:
        limit = len(driver.find_element(By.CLASS_NAME, "custom-links-pagination").find_elements(By.TAG_NAME, "nobr"))
    except:
        pass
    users = driver.find_element(By.CLASS_NAME, "standings").find_elements(By.TAG_NAME, "tr")
    for i in range(1, len(users) - 1):
        user = users[i].find_elements(By.TAG_NAME, "td")
        user_rank = user[0].text
        user_name = user[1].find_element(By.CLASS_NAME, "rated-user").text
        problems = []
        if not haveHeader:
            haveHeader = True
            sheet.append(doHeader(len(user) - 4))
        for ii in range(4, len(user)):
            problem = user[ii]
            try:
                isRejected = problem.find_element(By.CLASS_NAME, "cell-rejected")
                problems.append(isRejected.text if isRejected.text != ' ' else 0)
            except:
                problems.append(problem.find_element(By.CLASS_NAME, "cell-accepted").text)
        user_rank = user_rank if user_rank != ' ' else "*"
        sheet.append([user_rank, user_name] + problems)

workbook.save(f"contest-{contestId}.xlsx")
print("Done !")
end_time = time()
elapsed_time = end_time - start_time
print(f"\033[92mTime taken: {elapsed_time:.2f} seconds\033[0m")
driver.quit()
