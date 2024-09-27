import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = 'igbprogramming@gmail.com'
EMAIL_PASSWORD = 'qgpieyzreoqdelld'
RECIPIENT_EMAIL = ['igna19bg@gmail.com', 'iballest@uoguelph.ca', 'adrian168.10@gmail.com', 'emma.devr@gmail.com', 'petros@uoguelph.ca']
#RECIPIENT_EMAIL = 'adrian168.10@gmail.com'

subject = 'Dirty Dishes'
body = 'There are dirty dishes inthe sink.\n Please clean them!!!'

def SendEmail(subject, body):
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = ', '.join(RECIPIENT_EMAIL)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    text = message.as_string()

    #smtp connection
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
    return

def ProcessData(data, threshold):
    try:
        distanceVal = float(data)

    except ValueError:
        print('Invalid data format. Not a numeric value.')
        return

    if distanceVal < threshold:
        SendEmail(subject, body)
        return True
    
    else:
        return False
