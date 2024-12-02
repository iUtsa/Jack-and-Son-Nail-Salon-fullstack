import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_smtp(subject, body, to_email):

    sender_email = "abishekkumargiri0@gmail.com"
    sender_password = "fcwa cfha gyus tcuw"

    smtp_server = "smtp.gmail.com"
    smtp_port = 587


    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    server.sendmail(sender_email, to_email, msg.as_string())
    print("Email sent successfully to", to_email)


    server.quit()


send_email_smtp(
    subject="Booking Confirmation",
    body="Your booking is confirmed! Thank you for choosing us.",
    to_email="giriabi08@gmail.com"
)
