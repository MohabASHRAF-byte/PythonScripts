import subprocess
import time
from itertools import zip_longest
from subprocess import Popen, PIPE
import requests
from bs4 import BeautifulSoup
# request the url
def Requesting(number, char):
    url = f"https://codeforces.com/contest/{number}/problem/{char}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ScrappedInputt = soup.find_all("div", attrs={"class", "input"})
    ScrappedOutputt = soup.find_all("div", attrs={"class", "output"})
    return ScrappedInputt, ScrappedOutputt
# takes one parameter first the scrapped input list
def Get_input(codeInput):
    Test_Cases = []
    flag = True
    for test in range(len(codeInput)):
        Get_Test = codeInput[test].find("pre")
        Full_TestCase = []
        for i in range(len(Get_Test)):
            if not (i & 1):
                find = f"test-example-line test-example-line-even test-example-line-{i}"
            else:
                find = f"test-example-line test-example-line-odd test-example-line-{i}"
            lines = Get_Test.find_all("div", attrs={"class": find})
            if len(lines) == 0:
                break
            flag = False
            for line in lines:
                Full_TestCase.append(line.get_text().strip())
        if len(Full_TestCase) == 0:
            break
        Test_Cases.append(Full_TestCase)
    #################
    if flag:
        for i in range(len(codeInput)):
            t = []
            ff = codeInput[i].find("pre")
            st = str(ff)
            nst = st[5:-6]
            test = []
            for ii in nst.split("<br/>"):
                if not len(ii) == 0:
                    test.append(ii)
            for ii in test:
                for iii in ii.split("\n"):
                    if not len(iii) == 0:
                        t.append(iii)
            Test_Cases.append(t)
    return Test_Cases
# uses to run the program and return list of the output
def Run_program(Input_Test, path):
    result = subprocess.run(["g++", "-std=c++20", path, "-o", "program"], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    p = Popen(["program"], stdout=PIPE, stdin=PIPE)
    for line in Input_Test:
        p.stdin.write(line.encode())
        p.stdin.write("\n".encode())
    p.stdin.flush()
    res = p.stdout.readlines()
    program_outputt = []
    for i in res:
        program_outputt.append(i.decode().strip())
    return program_outputt
# uses to get the output for codeforces
def Get_Output(output):
    temp = []
    scrapped = []
    for i in range(len(output)):
        find_line = output[i].get_text()[6:].strip().split("\n")
        for ii in find_line:
            temp.append(ii)
        ss = []
        for ii in temp:
            if not len(ii.strip()) == 0:
                ss.append(ii.strip())
        scrapped.append(ss)
        temp = []
    return scrapped
# to check the identity of the two outputs
def Check(P_output, C_Output, cnt):
    flag4 = True
    flag5 = True
    for Program_Test, Codeforces_Test in zip_longest(P_output, C_Output, fillvalue=None):
        flag5 = True
        if Program_Test is None:
            Program_Test = ""
            flag4 = False
            flag5 = False
        if Codeforces_Test is None:
            Codeforces_Test = ""
            flag4 = False
            flag5 = False
        if Program_Test is None:
            Program_Test = ""
        for p_line, c_line in zip_longest(Program_Test, Codeforces_Test, fillvalue=None):
            if p_line is None:
                p_line = ""
            if c_line is None:
                c_line = ""
                flag4 = False
                flag5 = False
            for p, c in zip_longest(p_line.split(" "), c_line.split(" ")):
                if (p == c) and not p is None and not len(p) == 0:
                    print("\033[32m" + str(c) + "\033[0m", end=" ")
                else:
                    st = str(p if c is None else c)
                    print("\033[0;31m" + st + "\033[0m", end=" ")
                    flag4 = False
                    flag5 = False
            print("")
        if flag5:
            print("\033[1;32m" + f"Test {cnt} passed successfully !!" + "\033[0m")
        else:
            print("\033[1;31m" + f"Test {cnt} Failed !!" + "\033[0m")
        cnt += 1
    return flag4
# main
def main():
    x = input("Enter contest number ")
    y = input("Enter problem number ")
    path=r"C:\Users\amoha\CLionProjects\untitled1\main.cpp"
    ScrappedInput, ScrappedOutput = Requesting(x, y)
    start_time = time.time()
    CodeForcesTests = Get_input(ScrappedInput)
    CodeForcesOutput = Get_Output(ScrappedOutput)
    program_output = []

    for Test in CodeForcesTests:
        program_output.append(Run_program(Test, path))
    if Check(program_output, CodeForcesOutput, 1):
        print("\033[0;34m" + "Passed !!")
    else:
        print("\033[0;31mCheck again !!" + "\033[0m")

    print("\033[0;37m" + "Time taken by the program: ", round(time.time() - start_time, 2), "seconds")


###
main()
