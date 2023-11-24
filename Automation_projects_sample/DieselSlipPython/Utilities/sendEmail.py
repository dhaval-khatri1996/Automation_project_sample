import smtplib
from config import gmailUsername, gmailPassword
from Utilities.logger import log
from email.message import EmailMessage

def sendMail(to,subject,message):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = gmailUsername
    msg['To'] = to
    try:
        log("info", message)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmailUsername, gmailPassword)
        response = smtp_server.send_message(msg)
        smtp_server.close()
        log("info","Email sent successfully! " + str(response))
    except Exception as ex:
        log("ERROR","Could not send mail :- "+str(ex))
