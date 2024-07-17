
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app, session
import requests

# Function to generate a random six-digit OTP
def generate_otp():
    otp = random.randint(100000, 999999)
    return otp

# Function to establish an SMTP connection
def get_smtp_connection():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    return server

# Function to compose an email with OTP
def compose_email(from_email, to_email, otp):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'One-Time Password (OTP) Verification'

    body = f'''
    Dear User,

    Your One-Time Password (OTP) for verification is: {otp}.

    Please use this OTP to complete your verification process.

    Note: This OTP is valid for a limited time and should not be shared with anyone. 
    If you did not request this OTP, please ignore this email.

    Regards,
    e-Saksham
    '''
    msg.attach(MIMEText(body, 'plain'))
    
    return msg

def send_email(to_email):
    # Prepare the request payload
    API_KEY = current_app.config['ELASTICMAIL_API_KEY']
    SEND_ENDPOINT = current_app.config['ELASTICMAIL_API_URL']
    template_name = 'OTP'
    otp = generate_otp()
    username = session.get('user_name')
    merge_data = {'name': username, 'otp': otp}
    payload = {
        'apikey': API_KEY,
        'template': template_name,
        'to': to_email,
        'merge_source': merge_data,  # Optional merge data for template variables
        'merge': True,
        'from':'noreply.esaksham@gmail.com',
        'isTransactional': True,
        'subject': "OTP Verification",
        'fromName': "E-Saksham"
    }
    if merge_data:
        for key, value in merge_data.items():
            payload[f'merge_{key}'] = value
    try:
        # Send the POST request to the Elastic Email API to send email with the template
        response = requests.post(SEND_ENDPOINT, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Email sent successfully!")
            print(response.text)
            return {'otp':otp}
        else:
            print("Failed to send email. Status code:", response.status_code)
            print("Response:", response.text)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None
# Function to send email with OTP
# def send_email(email):
#     gmail_user = 'nimish.colab@gmail.com'  # Replace with your Gmail address
#     gmail_password = 'sinc worq ocvq fmdp'  # Replace with your app password
    
#     otp = generate_otp()
#     msg = compose_email(gmail_user, email, otp)
    
#     try:
#         server = get_smtp_connection()
#         server.login(gmail_user, gmail_password)
#         server.sendmail(gmail_user, email, msg.as_string())
#         return {'otp': otp}
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#     finally:
#         if 'server' in locals():
#             server.quit()  # Close the SMTP connection
