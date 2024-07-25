from email.mime.text import MIMEText
import smtplib

email = "telemedconnectdev@gmail.com"
password = "qrum eaon zpck tnub"

smtp_server = "smtp.gmail.com"
smtp_port = 587


def send_email(to_email, subject, message):

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to_email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)

    server.send_message(msg)
    server.quit()

