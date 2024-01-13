import requests as req
import csv
from bs4 import BeautifulSoup
def DG(x):
    for xxx in x:
        print(xxx)
def DT(x):
    for xxx in x:
        print(xxx.get_text())
def DS(x):
    for xxx in x:
        print(xxx.get_text().strip())

page_number=0
data=[]
x =input(f"Enter the job you want to search\t")
while True:
    url=f"https://wuzzuf.net/search/jobs/?a=navbg&q={x}&start={page_number}"
    response =req.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    #getting job name
    jobs_names = soup.find_all('a' ,attrs = {"class":"css-o171kl","rel":"noreferrer"})
    job_names_list=[ i.get_text().strip()  for i in jobs_names]
    # get links for all jobs
    job_links=["https://wuzzuf.net"+i['href'] for i in jobs_names]
    #get companies name list
    Company_name=soup.find_all('a', attrs = {'class' : 'css-17s97q8' ,'rel':"noreferrer" })
    companies_name_list=[ i.get_text()[:-2] for i in Company_name]
    #get_location
    locations = soup.find_all("span" , attrs ={"class":"css-5wys0k"})
    locations_list =[i.get_text().strip() for i in locations]
    #creating data
    page_data=[]
    for job_name ,company_name ,location ,link in zip(job_names_list,companies_name_list,locations_list,job_links):
        temp=[job_name,company_name,location,link]
        page_data.append(temp)
    print(page_number)
    if len(page_data)==0:
        break
    else :
        for i in page_data:
            data.append(i)
        page_number+=1
print(f"{page_number} pages scraped")
with open(f"{x}.csv" ,'w',newline="",encoding='UTF-8') as wr:
    writer =csv.writer(wr)
    header=["Job Title" ,"Company","Location","Link"]
    writer.writerow(header)
    writer.writerows(data)





