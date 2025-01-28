import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email=
sender_password =
recipient_email =
subject =
body =

def send_email_simple(sender_email=sender_email, sender_password=sender_password, recipient_email=None, subject=None, body=None):
    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption

        # Log in to your Gmail account
        server.login(sender_email, sender_password)

        # Create the email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(message)

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()

send_email_simple(sender_email, sender_password, recipient_email, subject, body)