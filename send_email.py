import smtplib

sender = "86misiaczek86@gmail.com"
receiver = "86misiaczek86@gmail.com"
password = "pass"
subject = "Python email"
body = "My email"

#header
message = f"""From: Mike{sender}
To: Mike{receiver}
Subject: {subject}\n
{body}
"""

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()

try:
    server.login(sender,password)
    print("Logged in")
    server.sendmail(sender,receiver,message)
    print("Email has been sent")

except smtplib.SMTPAuthenticationError:
    print("unable to login")