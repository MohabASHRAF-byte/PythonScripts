from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from random import randint as rand

# Replace these with your Codeforces credentials
username = "username"
password = "password"
# add trainees name
users = [
    "trainee1",
    "trainee2",
    "trainee3",
    "trainee4"
]
driver = webdriver.Chrome()
driver.get("https://codeforces.com/enter")
username_input = driver.find_element(By.ID, "handleOrEmail")
password_input = driver.find_element(By.ID, "password")
remember = driver.find_element(By.ID, "remember")
submit_button = driver.find_element(By.CLASS_NAME, "submit")
username_input.send_keys(username)
sleep(rand(1, 3))
password_input.send_keys(password)
sleep(rand(1, 3))
submit_button.click()
sleep(3)

for u in users:
    driver.get(f"https://codeforces.com/profile/{u}")
    sleep(3)
    try:
        isFried = driver.find_element(By.TAG_NAME, "h1").find_elements(By.CSS_SELECTOR, ".addFriend.friendStar")
    except:
        print(f"Couldn't find {u}")
        continue
    sleep(rand(1, 2))
    if len(isFried) != 0:
        isFried[0].click()
    sleep(rand(1, 4))
sleep(5)
driver.quit()
