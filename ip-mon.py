
from email.message import EmailMessage
import smtplib
import urllib.request
import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
import time


device = "Waianae-Pi"
recipients = ["admin-action@okimotocorp.com"]
gmail_user = 'helpdesk@okimotocorp.com'
gmail_password = 'jbjyloxswehguyak'
iplogfile = "iplog.txt"

iplog = open(iplogfile, "r")
last_external_ip = iplog.readline()
iplog.close()


def sendmail(subject, message):
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(gmail_user, gmail_password)
    msg = MIMEText(message)
    msg['Subject'] = f'{device} - {subject}'
    msg['From'] = gmail_user
    msg['To'] = ", ".join(recipients)
    smtpserver.sendmail(gmail_user, recipients, msg.as_string())
    smtpserver.quit()
def exec(args):
    return subprocess.Popen(args, shell=True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

external_ip = urllib.request.urlopen(
    'https://api.ipify.org').read().decode('utf8')
print(external_ip)
iplog = open(iplogfile, "w")
iplog.write(external_ip)
iplog.close()

today = datetime.datetime.now().strftime("%A, %b %d %Y %H:%M:%S %z")
arg = 'ip route list'
data = exec(arg)
arg = f'whois {external_ip}'
whodata = exec(arg)
msgtxt = (f'This is {device} waking up. \nToday is {today}.\n'
          f'My outside is IP {external_ip} and it was '
          f'{last_external_ip} when I last slept\n\n\n'
          f'{data}\n{whodata}'
          )
sendmail("Start up", msgtxt)

while True:
    time.sleep(90)
    try:
        print("looped")
        latest_ip = urllib.request.urlopen(
            'https://api.ipify.org').read().decode('utf8')
        if latest_ip != external_ip:
            arg = f'whois {latest_ip}'
            whodata = exec(arg)

            msgtxt = f'New IP: {latest_ip}, it was {external_ip}\n{whodata}'
            sendmail("IP Changed", msgtxt)

            external_ip = latest_ip

            iplog = open(iplogfile, "w")
            iplog.write(external_ip)
            iplog.close()
    except:
            print(f'{datetime.datetime.now().strftime(" % A, % b % d % Y % H: % M: % S % z")} - GET Fail')

