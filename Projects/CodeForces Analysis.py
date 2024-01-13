import requests
import datetime
from prettytable import PrettyTable
from time import sleep

handle = "Mohab"
res = requests.get(f"https://codeforces.com/api/user.info?handles={handle}").json()
req2 = requests.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=5000").json()
# info table
info_table = PrettyTable()
info_table.field_names = [" .", ". "]
for k, v in res['result'][0].items():
    if k == "lastOnlineTimeSeconds" or k == "registrationTimeSeconds".strip():
        datetime_obj = datetime.datetime.fromtimestamp(v)
        info_table.add_row([k, datetime_obj.strftime("%Y-%m-%d %H:%M:%S")])
    else:
        info_table.add_row([k, v])

# containers
scrapped_submissions = set()
rating = dict()
topics = dict()
programmingLanguage = dict()
marked = set()
type_marked = set()
verdict = dict()
virtualContests = set()
gyms = set()
# (name >><<, participants >> <<,team name >><<, rank >><<, difficulty >> <<, ,total >><<,solved>><<)
contests = set()


# name>> rank  total>> solved>>
# functions
def add_element(element, mp: dict):
    if element in mp:
        mp[element] += 1
    else:
        mp[element] = 1


for idx, submission in enumerate(req2['result']):

    # calculate programming language
    add_element(submission['programmingLanguage'], programmingLanguage)
    # calculate verdict
    add_element(submission['verdict'], verdict)
    if submission['verdict'] == "OK":
        # creating id for each problem
        ID = str(submission['contestId']) + submission['problem']['index']
        # check if it got acc before
        if ID not in marked:
            # add rating
            try:
                add_element(submission['problem']['rating'], rating)
            except:
                pass
            # add tags
            for tag in submission['problem']['tags']:
                add_element(tag, topics)
            marked.add(ID)

        # add this submission to submissions list
        scrapped_submissions.add((submission['contestId'], submission['id'], submission['problem']['name']))
        # mark problem
    # VIRTUAL CONTESTS
    else:
        continue
    if submission['author']['participantType'] == "VIRTUAL":
        virtualContests.add(submission['contestId'])
    type_marked.add((ID, submission['author']['participantType']))

# sorting rating table
li = []
for k, v in rating.items():
    li.append((k, v))
li.sort()
rating_table = PrettyTable()
rating_table.field_names = ["Rating", "solved"]
for i in li:
    rating_table.add_row([i[0], i[1]])
# sorting topics table
li = []
for k, v in topics.items():
    li.append((v, k))
li.sort()
topics_table = PrettyTable()
topics_table.field_names = ["Topic", "solved"]

li.sort(reverse=True)
for i in li:
    topics_table.add_row([i[1], i[0]])
temp = 0

for id in virtualContests:
    sleep(.5)
    try:
        # check if gym
        if id > 2000:
            # gym
            user_result = requests.get(
                f'https://codeforces.com/api/contest.standings?contestId={id}&handles={handle};&showUnofficial=true').json()
            if user_result['status'] == "OK":
                gym = user_result['result']['rows'][0]
                contestName = user_result['result']['contest']['name']
                diff = user_result['result']['contest']['difficulty']
                members = f"{handle}"
                # getting members
                try:
                    teamName = gym['party']['teamName']
                except KeyError:
                    teamName = "individual"
                Rank = gym['rank']
                for mem in gym['party']['members']:
                    if mem['handle'] != handle:
                        members += f" - {mem['handle']}"
                # getting solved problem
                total = len(user_result['result']['problems'])
                solved = 0
                for problem in user_result['result']['problems']:
                    idd = str(problem['contestId']) + (problem['index'])
                    solved += ((idd, 'VIRTUAL') in type_marked)
                gyms.add((contestName, diff, teamName, members, total, solved, Rank))
        else:
            # contest
            user_result = requests.get(
                f'https://codeforces.com/api/contest.standings?contestId={id}&handles={handle};&showUnofficial=true').json()
            if user_result['status'] == "OK":
                contestName = user_result['result']['contest']['name']
                Rank = user_result['result']['rows'][0]['rank']
                # getting solved
                total = len(user_result['result']['problems'])
                solved = 0
                for problem in user_result['result']['problems']:
                    idd = str(problem['contestId']) + (problem['index'])
                    solved += ((idd, 'VIRTUAL') in type_marked)
                tup = (contestName, Rank, solved, total)
                contests.add(tup)
    except Exception as e:
        print(id)
# gyms table
gyms_table = PrettyTable()
li = list()
for i in gyms:
    li.append([i[6], i[1], i[2], i[3], i[4], i[5], i[0]])
li.sort()
gyms_table.field_names = ["Name", "diff", "teamName", "members", "total", "solved", "Rank"]

for i in li:
    gyms_table.add_row([i[6], i[1], i[2], i[3], i[4], i[5], i[0]])

# contests table
contests_table = PrettyTable()

contests_table.field_names = ["Name", "Rank", "solved", "total"]
li = list()

for i in contests:
    li.append([i[1], i[0], i[2], i[3]])
li.sort()
for i in li:
    contests_table.add_row([i[1], i[0], i[2], i[3]])
print(info_table)
print(rating_table)
print(topics_table)
print(f"Number of gyms : {len(gyms)} ")
print(gyms_table)
print(f"Number of contests : {len(contests)} ")
print(contests_table)
