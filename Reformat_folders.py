import os
import shutil
import time

#           0           1          2        3       4        5           6             7        8
folders = ['videos', 'photos', 'office', 'code', 'pdf', 'compressed', 'windows apps', 'music', 'others', '.idea']
paths = []

execution = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]

video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2',
                    '.m2v', '.mpg2', '.mp2v', '.mpv', '.divx', '.xvid', '.rm', '.rmvb', '.vob', '.swf', '.f4v', '.m2ts',
                    '.mts', '.ts', '.mxf', '.ogv', '.ogg', '.ogm', '.mod', '.tod', '.dat', '.vro', '.dvr-ms', '.ts',
                    '.trp', '.wtv', '.asf', '.asx', '.amv', '.drc', '.gvi', '.pva', '.tivo', '.wtv', '.nsv', '.pss',
                    '.rmm', '.smk', '.bik', '.cine', '.roq', '.fli', '.flc', '.flic', '.f4p', '.f4a', '.f4b', '.f4m',
                    '.f4v']

photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.raw', '.svg', '.webp', '.heif', '.heic',
                    '.psd', '.ai', '.eps', '.indd', '.svgz', '.xcf', '.ico', '.dng']
code_extensions = ['.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.js', '.php', '.rb', '.swift', '.go', '.rust',
                   '.lua', '.pl', '.vb', '.ts', '.dart', '.sh', '.sql', '.json', '.xml', '.ipynb']
office_extensions = ['.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.csv', '.odt', '.ods', '.odp', '.rtf']
pdf_extensions = ['.pdf']
compressed_extensions = ['.zip', '.rar', '.tar', '.gz', '.7z', '.xz', '.bz2', '.tar.gz', '.tar.bz2', '.tar.xz']
windows_extensions = ['.exe']
music_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']

all_extensions = [set(video_extensions), set(photo_extensions), set(office_extensions), set(code_extensions),
                  set(pdf_extensions), set(compressed_extensions), set(windows_extensions)
    , set(music_extensions)
                  ]


def create_folders():
    curr = os.getcwd()
    all_folders = [x.lower() for x in os.listdir(curr)]
    for folder in folders:
        if not (folder.lower() in all_folders):
            os.mkdir(folder)
        paths.append(curr + "\\" + folder)


mainPath = os.getcwd()


def do_work():
    currDir = os.getcwd().split('\\')[-1]
    currPath = os.getcwd()

    for file in os.listdir(currPath):
        # check if the current folder is one of the created folders not to scan
        if file.lower() in folders and currPath == mainPath:
            continue
        #     check if the file is directory then scan it
        if os.path.isdir(file):
            NewPath = currPath + "\\" + file
            os.chdir(NewPath)
            do_work()
            continue
        # if file then get it's full path
        file_path = currPath + '\\' + file
        # classify files
        flag = False
        for ex in range(len(all_extensions)):
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in all_extensions[ex]:
                execution[ex].add(file_path)
                flag = True
                break
        if not flag:
            execution[8].add(file_path)

    # back to the previous directory
    if not (currPath == mainPath):
        os.chdir("..")


def execute():
    #
    for i in range(len(folders) - 1):
        cnt = 0
        folder_elements = set(os.listdir(paths[i]))
        for element in execution[i]:
            if "Reformat_folders.py" in element:
                continue
            elementName = element.split('\\')[-1]
            number = 1
            if elementName in folder_elements:
                temp = elementName.split('.')
                if len(temp) < 2:
                    shutil.move(element, paths[8] + '\\' + elementName)
                    continue
                else:
                    elementName = temp[0] + '_' + str(number) + '.' + temp[1]
                    while elementName in folder_elements:
                        temp = elementName.split('.')
                        elementName = temp[0][:-1] + str(number) + '.' + temp[1]
                        number += 1
            folder_elements.add(elementName)
            shutil.move(element, paths[i] + '\\' + elementName)
            cnt += 1
        print(folders[i], cnt)


def delete_dir():
    currPath = os.getcwd()
    currDir = os.getcwd().split('\\')[-1]
    for directory in os.listdir(currPath):
        if (directory.lower() in folders) and mainPath == currPath:
            continue
        if os.path.isdir(directory):
            tempPath = currPath + "\\" + directory
            os.chdir(tempPath)
            delete_dir()
    if not (currPath == mainPath):
        os.chdir("..")
        if (currDir.lower() in folders) and mainPath == currPath:
            pass
        else:
            try:
                os.rmdir(currPath)
            except PermissionError:
                pass


def main():
    start_time = time.time()
    create_folders()
    do_work()
    execute()
    delete_dir()
    print(f"\033[92mTotal execution time: {time.time() - start_time:.2f} seconds")


main()
