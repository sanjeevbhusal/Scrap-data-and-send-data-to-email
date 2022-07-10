import os
from smtplib import SMTP, SMTPException
from dotenv import load_dotenv
from email.mime.text import  MIMEText  
from email.mime.multipart import MIMEMultipart

load_dotenv()

sender = os.getenv("sender_email")
password = os.getenv("sender_password")
receiver = os.getenv("receiver_email")
host = os.getenv("host")
port = os.getenv("port")

message = MIMEMultipart("alternative")
message["SUBJECT"] = "Hi There"
message["TO"] = receiver
message["FROM"] = sender

text = """\
Hi,
How are you?
I am trying to learn to send email using python"""

with open("index.html", "r") as f:
    html = f.read()

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)


def send_email():
    """
    Send an email using the credentials defined before

    Parameters
    ----------
    message : str
        content to send in the message
    """
    
    with SMTP(host=host, port=port) as smtp:
        try:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, message.as_string() )
            print("Succesfully sent email")
        except SMTPException:
            print("Error: unable to send email")
            
              
if __name__ == "__main__":
    print("Sending a plain text email")
    send_email()
        