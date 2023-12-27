import requests
from collections import defaultdict
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

handle1 = defaultdict()
# set to mark solved problems for handle number 2
st1 = set()
problems = list()
driver = webdriver.Chrome()


def get_data(sync: str, syncWith: str):
    global problems, st1
    req1 = requests.get(f"https://codeforces.com/api/user.status?handle={sync}&from=1&count=5000").json()
    # sleep(2)
    req2 = requests.get(f"https://codeforces.com/api/user.status?handle={syncWith}&from=1&count=5000").json()
    for idx, submission in enumerate(req1['result']):
        contestId = submission['contestId']
        problemIdx = submission['problem']['index']
        problemId = str(contestId) + str(problemIdx)
        if submission['verdict'] == 'OK' and not (problemId in st1):
            st1.add(problemId)

    # #  get all acc for the account to sync with in problems, st2
    for idx, submission in enumerate(req2['result']):
        contestId = submission['contestId']
        problemIdx = submission['problem']['index']
        submissionId = submission['id']
        verdict = submission['verdict']
        problemId = str(contestId) + str(problemIdx)
        if submission['verdict'] == 'OK' and not (problemId in st1):
            st1.add(problemId)
            problems.append([str(contestId), str(problemIdx), str(submissionId)])


def codeforces_login(username: str, password: str):
    global driver
    driver.get("https://codeforces.com/enter")
    username_input = driver.find_element(By.ID, "handleOrEmail")
    password_input = driver.find_element(By.ID, "password")
    submit = driver.find_element(By.CLASS_NAME, "submit")
    username_input.send_keys(username)
    password_input.send_keys(password)
    sleep(1)
    submit.click()
    sleep(3)


def get_cpy(contestId: str, submissionId: str):
    global driver
    driver.get(f"https://codeforces.com/contest/{contestId}/submission/{submissionId}")
    cpy = driver.find_element(By.CSS_SELECTOR, 'div[title="Copy"]')
    cpy.click()
    sleep(1)


def submit_problem(contestId: str, problemId: str):
    global driver
    driver.get(f"https://codeforces.com/contest/{contestId}/submit/{problemId}")
    txt = driver.find_element(By.CSS_SELECTOR, 'div[class="ace_content"]')
    txt.click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
    submit_button = driver.find_element(By.ID, "singlePageSubmitButton")
    submit_button.click()
    sleep(2)


def main():
    username = "account1"
    password = "password"
    codeforces_login(username, password)
    get_data("account1", "account2")
    for contestId, problemIdx, submissionId in problems:
        get_cpy(contestId, submissionId)
        submit_problem(contestId, problemIdx)
        print(f"problem {contestId + problemIdx} submitted")
    sleep(500)


if __name__ == '__main__':
    main()
