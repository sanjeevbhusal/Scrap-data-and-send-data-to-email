import os
from smtplib import SMTP, SMTPException
from dotenv import load_dotenv
from email.mime.text import  MIMEText  
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from scrapper import scrape_news_list

load_dotenv()


def send_email(sender, receiver, password, message, host, port):
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
            smtp.sendmail(sender, receiver, message.as_string())
            return "Succesfully sent email"
        except SMTPException:
            return "Error: unable to send email"
        
def prepare_email_message(sender, receiver, html_file):
    message = MIMEMultipart("alternative")
    message["SUBJECT"] = "Hi There"
    message["TO"] = receiver
    message["FROM"] = sender
    html_data = MIMEText(html_file, "html")
    message.attach(html_data)
    return message

                         
def generate_html_file(news_list):
    with open("templates/index.html", "r") as f:
        html = f.read()
    template = Template(html)
    return template.render(news_list = news_list)


def get_email_credentials():
    sender = os.getenv("sender_email")
    password = os.getenv("sender_password")
    receiver = os.getenv("receiver_email")
    host = os.getenv("host")
    port = os.getenv("port")
    return sender, password, receiver, host, port


if __name__ == "__main__":
    sender, password, receiver, host, port = get_email_credentials()
    news_list = scrape_news_list()
    html_file = generate_html_file(news_list)
    message_obj = prepare_email_message(sender, receiver, html_file)
    
    print("Sending email")
    response_message = send_email(sender, receiver, password, message_obj, host, port)
    print(response_message)

        