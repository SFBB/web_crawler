import requests
from pprint import pprint
from bs4 import BeautifulSoup
import csv
import time
import copy

for page in range(1, 1793):
    print(str(page)+" / 1793")
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get("https://novelcom.syosetu.com/impression/list/ncode/302237/?p="+str(page), headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            # print(soup.prettify())
            with open(str(page)+".html", "w") as html:
                html.write(soup.prettify())
            comments = []
            sections = soup.find_all(class_="waku")
            for section in sections:
                if section.find_all(class_="res"):
                    com = ""
                    comments_reader = section.find_all(class_="comment")
                    # print(len(comments))
                    for i in range(len(comments_reader)-1):
                        com += comments_reader[i].text + "\n"
                    com = com.replace("\n", "\xfe")
                    res = section.find_all(class_="res")[0].find_all(class_="comment")[0].text
                    res = res.replace("\n", "\xfe")
                    # print(res)
                    date_0 = section.find_all(class_="comment_info")[0].text.replace("\n", "\xfe")
                    # print(part)
                    date_1 = section.find_all(class_="comment_info")[1].text.replace("\n", "\xfe")
                    comments.append({"reader": com, "author": res, "date_0": date_0, "date_1": date_1, "page": str(page)})
            # comments_list = soup.find_all(class_="waku")[0].find_all(class_="comment")
            # print(comments)
            with open("comments.csv", "a", newline="") as file:
                writer = csv.writer(file)
                # writer.writerow(news_data[0].keys())
                for i in range(len(comments)):
                    new_row = []
                    for key in comments[0].keys():
                        new_row.append(comments[i][key])
                    writer.writerow(new_row)
            # print(comments)
            # news_data = []
            break
        except Exception as e:
            print(e)
            time.sleep(1)
