
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import session,url_for
import os

# Function to generate a random six-digit OTP
def generate_otp():
    otp = random.randint(100000, 999999)
    return otp

# Function to establish an SMTP connection
def get_smtp_connection():
    smtp_server = 'smtp-relay.brevo.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    return server

# Function to compose an email with OTP


# def send_email(recipient_email):
#     # Configure API key authorization
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
#     otp = generate_otp()
#     username = session.get('user_name')
#     params = {"otp":otp,"name":username}
#     # Create an instance of the API class
#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#     template_id = 1
#     # Define the sender and recipient
#     sender = {"name": "E-Saksham Learning", "email": "noreply.esaksham@gmail.com"}
#     to = [{"email": recipient_email}]

#     # Create the email using the template
#     send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#         to=to,
#         template_id=template_id,
#         params=params,
#         sender=sender
#     )

#     try:
#         # Send the email
#         api_response = api_instance.send_transac_email(send_smtp_email)
#         print(api_response)
#         return {"otp":otp}
#     except ApiException as e:
#         print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
#         return False


def send_email(recipient_email):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "noreply.esaksham@gmail.com"  # Your sender email
    sender_password = 'hcpe tquf mabp bfyl'  # Your email password

    otp = generate_otp()
    username = session.get('user_name')  # Replace with the actual username from your session

    # Create the email content
    subject = "OTP Verification"
    
    template = f"""
            Hello {username},
            
            Your One-Time Password (OTP) for verification is:{otp}.
            
            Please use this OTP to verify your identity.
            
            If you didn't request this OTP, please ignore this email.
            
            Regards,
            Yukt Saksham (Digital Learning Platform)
        """
    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(template, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)  # Log in to the server
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
            print("Email sent successfully!")
            return {"otp": otp}
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
    
#'''hcpe tquf mabp bfyl'''
