from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep


# functions
def login(bot, user, pas):
    wait = WebDriverWait(bot, 10)
    element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Phone number, username, or email']")))
    user_input = bot.find_element(By.CSS_SELECTOR, "input[aria-label='Phone number, username, or email']")
    password_input = bot.find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
    login_btn = bot.find_element(By.CSS_SELECTOR, "button[type='submit']")

    # send user pass and login and wait for 5 seconds to load the page
    user_input.send_keys(user)
    password_input.send_keys(pas)
    login_btn.click()
    sleep(5)
    return bot


def like(bot):
    try:
        tmp2 = bot.find_element(By.CLASS_NAME, '_aatl')
        actions = ActionChains(bot)
        actions.double_click(tmp2).perform()
    except:
        return True
    return False


def like_btn_click(bot):
    try:
        tmp = bot.find_element(By.CSS_SELECTOR, 'svg[color="rgb(255, 48, 64)"]')
        print(tmp)
        tmp.click()
        sleep(3)
        print("clicked")
        return 0
    except:
        print("ima out")
        return 1


def get_next(bot):
    try:
        sleep(1)
        tmp1 = bot.find_element(By.CSS_SELECTOR, 'svg[aria-label="Next"]')
        tmp1.click()
        sleep(1)
    except:
        return True
    return False


def move_to_profile(bot, u):
    bot.get(f"https://www.instagram.com/{u}/")


def get_first_photo(bot, u):
    wait = WebDriverWait(bot, 10)
    element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "_aagu")))
    print(element)
    bot.get(f"https://www.instagram.com/{u}/")
    tmp = bot.find_element(By.CLASS_NAME, '_aagu')
    tmp.click()
    sleep(5)


def main():
    fail = False
    os.environ['PATH'] += r"F:/Python/selenuim/drivers"
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    print('1 - like \n'
          '2 - dislike\n ')
    xx = int(input())
    print("1/ login with user and password\n2/login with facebook")
    x = int(input())
    user = "_mohab_ashraf_0"
    if x == 1:
        acc_user = "mohafdljfdd"
        acc_pas = "fasdfasdfasdfasdfdasf"
        driver.get("https://www.instagram.com/")
        login(driver, acc_user, acc_pas)

    else:
        driver.get("https://www.instagram.com/")
        sleep(100)

    move_to_profile(driver, user)
    get_first_photo(driver, user)
    cnt = 0

    if x == 1:
        while not fail:
            fail |= like(driver)
            fail |= get_next(driver)
            cnt += 1
            print(cnt)
    else:
        while not fail:
            fail |= like(driver)
            sleep(1)
            like_btn_click(driver)
            sleep(1)
            fail |= get_next(driver)
            cnt += 1
            print(cnt)
            
        s = "liked" if xx == 1 else "disliked"
        print(f"{cnt} photos {s} successfully")
        sleep(1000)


main()
