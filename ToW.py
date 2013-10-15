import random
from smtplib import SMTP_SSL
import email
import imaplib
import time

f = open('data','r')
datas = f.readlines()
for n in range(len(datas)):
    datas[n] = datas[n].strip('\n')
numbers = {datas[2]:datas[3],
        datas[4]:datas[5],
        datas[6]:datas[7],
        datas[8]:datas[9],
        datas[10]:datas[11]
        }

def login_check():
    global datas
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(datas[0],datas[1])
    return mail

def check_new_mail(mail):
    mail.select('INBOX')
    return int(mail.select('INBOX')[1][0])

def purge_inbox(mail):
    typ, data = mail.search(None, 'ALL')
    for num in data[0].split():
           mail.store(num, '+FLAGS', '\\Deleted')
    mail.expunge()

def logout_check(mail):
    mail.close()
    mail.logout()

def send(message):
    global datas
    global numbers
    s = SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    s.login(datas[0],datas[1])
    for n in numbers:
        s.sendmail(datas[0], numbers[n], str(message))
    s.quit

def pick_place():
    places = ['Schlotzky\'s','Coco\'s','Tap House','Domino\'s','Dobie',
            'Teji\'s','Chipotle','Pita pit','Which wich','Austin pizza',
            'Kismet','Big bite','Noodles','Mellow Mushroom','Fuzzy\'s',
            'Kerbey Lane','Halal Bros','Five Guys']
    return random.choice(places)

if __name__ == '__main__':
    needed = int(raw_input('NUMBER OF OBJECTIONS NEEDED TO REPICK: '))
    objections = 0
    while True:
        objections = 0
        send(pick_place())
        print 'Waiting 2 minutes for objections...'
        time.sleep(120)
        mail = login_check()
        objections = check_new_mail(mail)
        purge_inbox(mail)
        logout_check(mail)
        if objections < needed:
            break



