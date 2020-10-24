import smtplib
import requests
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup
import csv
import time
import datetime
import copy
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'username@gmail.com' #change this to match your gma$
GMAIL_PASSWORD = 'password'  #change this to match your gmail password

class Emailer:
    def sendmail(self, recipient, subject, content, attachments=[]):


        message = MIMEMultipart()
        message['From'] = "Name<"+GMAIL_USERNAME+">"
        message['To'] = recipient
        message['Subject'] = subject

        message.attach(MIMEText(content, 'plain'))
        if attachments != []:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(
                        file.read(),
                        Name=basename(attachment)
                    )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
                message.attach(part)
            
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD) #login with mail_id and password
        text = message.as_string()
        session.sendmail(GMAIL_USERNAME, recipient, text)
        session.quit()


# count = 0
# for page in range(1, 25):
    # print(str(count)+" / 23")
with open("word_number.txt", "r") as file:
    old_word_number = file.read()
    # print(old_word_number)
    old_word_number = int(old_word_number)

while True:
    try:
        # print(1)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get("https://ncode.syosetu.com/novelview/infotop/ncode/n2267be/", headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup.prettify())
        # with open("narou_text_"+str(page)+".html", "w") as html:
        #     html.write(soup.prettify())
        # print(2)
        # for br in soup.find_all("br"):
        #     br.replace_with("\n")
        # comments = []
        table = soup.find_all(id="noveltable2")[0]
        new_table = pd.DataFrame(columns=range(0,2), index = [0]) # I know the size 

        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                new_table.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
        word_number = int(new_table[0][0].replace(",", "").replace("文字", ""))
        if word_number > old_word_number:
            words = word_number - old_word_number
            # send email with words
            print("sadasd")
            sender = Emailer()

            sendTo = 'receiver@email.com'
            emailSubject = "Tappei have updated WN!"
            emailContent = "He added "+str(words)+" words! Original word number is "+str(old_word_number)+"words, and current word number is "+str(word_number)+" words!\n\n\nYou can check this info on:\nhttps://ncode.syosetu.com/novelview/infotop/ncode/n2267be/#noveltable2,\n\nand read WN on:\nhttps://ncode.syosetu.com/n2267be/#c4e490f82661b73da494d6f6a7b6bb39.\n\n\n"
            sender.sendmail(sendTo, emailSubject, emailContent)
            with open("checking_history.txt", "a") as file:
                file.write(str(datetime.datetime.now())+", email has been sent to "+sendTo+"!\n")
            with open("word_number.txt", "w") as file:
                file.write(str(word_number))
            old_word_number = word_number
            with open("checking_history.txt", "a") as file:
                file.write(str(datetime.datetime.now())+", word number has been updated to "+str(word_number)+"!\n")
        else:
            pass
        with open("checking_history.txt", "a") as file:
            file.write(str(datetime.datetime.now())+", checking has been completed!\n")
        time.sleep(3600)
    except Exception as e:
        print(e)
        with open("checking_history.txt", "a") as file:
             file.write(str(datetime.datetime.now())+", error occured: "+str(e)+"!\n")
        time.sleep(1)
