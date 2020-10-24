import requests
from pprint import pprint
from bs4 import BeautifulSoup
import csv
import time
import copy

count = 0
for page in range(1, 167):
    print(str(count)+" / 165")
    while True:
        try:
            # print(1)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get("https://ncode.syosetu.com/n2267be/"+str(page)+"/", headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            # print(soup.prettify())
            with open("narou_text_"+str(page)+".html", "w") as html:
                html.write(soup.prettify())
            # print(2)
            for br in soup.find_all("br"):
                br.replace_with("\n")
            # comments = []
            subtitle = soup.find_all(class_="novel_subtitle")
            # place_index = subtitle[0].text.find("　")
            # if count+1 == int(subtitle[0].text[3:place_index]):
            #     count += 1
            if "リゼロＥＸ" not in subtitle[0].text and "断章" not in subtitle[0].text and "番外編" not in subtitle[0].text and "特別編" not in subtitle[0].text:
                count += 1
                all_text = ""
                par_count = 1
                while True:
                    par_text = soup.find_all(id="L"+str(par_count))
                    par_count += 1
                    # print(par_text)
                    # print(len(par_text))
                    # if par_text[0].text == "":
                    # print(par_count)
                    if len(par_text) == 0:
                        # print("text OK!")
                        break
                    all_text += par_text[0].text
                all_text = subtitle[0].text + "\n\n\n" + all_text
                with open("result.txt", "a") as file:
                    file.write(all_text)
            # print("OK!")
            break
        
                # print(count+1)
                # print(subtitle[0].text[3:place_index])
            # for section in sections:
            #     if section.find_all(class_="res"):
            #         com = ""
            #         comments_reader = section.find_all(class_="comment")
            #         # print(len(comments))
            #         for i in range(len(comments_reader)-1):
            #             com += comments_reader[i].text + "\n"
            #         com = com.replace("\n", "\xfe")
            #         res = section.find_all(class_="res")[0].find_all(class_="comment")[0].text
            #         res = res.replace("\n", "\xfe")
            #         # print(res)
            #         date_0 = section.find_all(class_="comment_info")[0].text.replace("\n", "\xfe")
            #         # print(part)
            #         date_1 = section.find_all(class_="comment_info")[1].text.replace("\n", "\xfe")
            #         comments.append({"reader": com, "author": res, "date_0": date_0, "date_1": date_1, "page": str(page)})
            # # comments_list = soup.find_all(class_="waku")[0].find_all(class_="comment")
            # # print(comments)
            # with open("comments.csv", "a", newline="") as file:
            #     writer = csv.writer(file)
            #     # writer.writerow(news_data[0].keys())
            #     for i in range(len(comments)):
            #         new_row = []
            #         for key in comments[0].keys():
            #             new_row.append(comments[i][key])
            #         writer.writerow(new_row)
            # # print(comments)
            # # news_data = []
            # break
        except Exception as e:
            print(e)
            time.sleep(1)
