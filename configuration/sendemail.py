import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask import render_template

def send_user_email(user_data):

    # SMTP server settings (example with Gmail SMTP server)
    smtp_server = os.getenv("SMTP_SERVER")  # Default to Gmail's SMTP server
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SMTP_USERNAME")
    sender_password = os.getenv("SMTP_PASSWORD")

    # Set up the MIME message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = user_data["contact"]["email"]
    message['Subject'] = "Mapua Parentlink Account Details"

    login_url = "malayanmindanao-test.blackboard.com"
    
    
    body = render_template('email_register.html',
                           given_name=user_data['name']['given'],
                           family_name=user_data['name']['family'],
                           user_name=user_data['userName'],
                           email=user_data['contact']['email'],
                           role=' '.join(user_data['institutionRoleIds']),
                           login_url=login_url)

    
    message.attach(MIMEText(body, 'html'))

    # Send the email
    try:
        gmail = smtplib.SMTP(smtp_server,smtp_port)
        gmail.starttls()
        gmail.login(sender_email,sender_password)
        gmail.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_contact_email(form):
    # SMTP server settings (example with Gmail SMTP server)
    smtp_server = os.getenv("SMTP_SERVER")  # Default to Gmail's SMTP server
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SMTP_USERNAME")
    sender_password = os.getenv("SMTP_PASSWORD")

    # Set up the MIME message
    message = MIMEMultipart()
    message['From'] = sender_email  # Sender email address
    message['To'] = form['admin_email']  # Recipient email (your email)
    message['Subject'] = f"Customer Concerns -- {form['contact_name']}"

    # Fix the body assignment to avoid tuple error
    body = f"""
        <h3> Details: </h3>
        <p> Name: {form['contact_name']} </p>
        <p> Email address: {form['user_email']} </p>
        <br>
        <h3> Message: </h3>
        {form['message']}
    """
    message.attach(MIMEText(body, 'html'))  # Ensure the body is sent as HTML

    # Send the email
    try:
        gmail = smtplib.SMTP(smtp_server, smtp_port)
        gmail.starttls()
        gmail.login(sender_email, sender_password)
        gmail.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")