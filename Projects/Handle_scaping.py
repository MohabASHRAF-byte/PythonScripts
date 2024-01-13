import requests
from bs4 import BeautifulSoup

x = input("Enter the handle\t")
url = "https://codeforces.com/profile/" + x
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# getting handle
try:
    h1s = soup.find("h1")
    # strip function to return the text without \n in the begin or in the end
    print(f"Handle : {h1s.get_text().strip()}")
    li = ["user-gray", "user-green", "user-cyan", "user-blue", "user-violet", "user-orange", "user-red",
          "user-legendary"]
    # getting rating
    spans = soup.find_all("span", attrs=li)
    rate_list = [i.getText() for i in spans]
    # for i in rate_list:
    #     print(i)
    if len(rate_list) == 0:
        print("UnRated")
    else:
        print(f"Current Rank  : {rate_list[0]} with {rate_list[1]}\n"
              f"max Rank :{rate_list[2][:-2]} with {rate_list[3]}")
    numbers = soup.find_all("div", attrs={"class": "_UserActivityFrame_counterValue"})
    days = soup.find_all("div", attrs={"class": "_UserActivityFrame_counterValue"})
    print(f"Total problems {days[0].get_text()[:-9]} solved")
except:
    print("Please enter valid user!!")
