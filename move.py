import os
import shutil

print(os.getcwd())
x = input("Enter search name \t")
nn = input("Enter folder name\t")
files = os.listdir()
if nn not in files:
    os.mkdir(nn)
cnt = 0
for filename in files:
    if x == filename:
        continue
    elif x in filename:
        shutil.copy(filename, nn)
        os.remove(filename)
        cnt += 1
print(f"{cnt} files moved !!")
