import requests

contest = "103176"
handles = ["Mohab", "ammar7018", "MoamenSherif"]


def do_work(Handle: str):
    req2 = requests.get(f"https://codeforces.com/api/user.status?handle={Handle}&from=1&count=1000000").json()
    for idx, submission in enumerate(req2['result']):
        if submission['verdict'] == "OK":
            if str(submission['contestId']) == contest:
                return False
    return True


flag = True
for handle in handles:
    if not do_work(handle):
        flag = False
        break
print("not valid") if not flag else print("valid")
