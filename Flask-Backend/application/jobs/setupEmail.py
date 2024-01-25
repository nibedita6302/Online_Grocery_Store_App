import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
from email.mime.multipart import MIMEMultipart
from ..jobs.createPDF import create_pdf

def sendEmail(receiver_email, email_type='reminder'):
    # Email account details
    sender_email = "nibedita.6302@gmail.com"
    app_password = "tjut zhyb jyuo vrum"  # Replace with your generated App Password

    # Set up the email details
    if email_type=='reminder':
        subject = "Grocery Store Reminder"
        body = f'''Dear {receiver_email.split('@')[0]}, 
        We see that you have not bought anything from Grocery Store.
        Please visit and have a look at you favourite products.

        Thank you
        Regards 
        Grocery Store Admin
        '''
    else:
        subject = "Monthly Report - Grocery Store"
        body = "Please find the below Monthly report PDF.\n Regards"


    # Create the MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, "plain"))

    if email_type=='report':
        # open the file to be sent  
        pdf=create_pdf()
        filename = f"{month}.pdf"
        month = datetime.now().strftime('%B')
        attachment = open(f"./PDF_Report/{pdf}", "rb") 
        
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
        
        # encode into base64 
        encoders.encode_base64(p) 
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        
        # attach the instance 'p' to instance 'msg' 
        message.attach(p) 

    # Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Start the TLS (Transport Layer Security) mode
        server.starttls()

        # Login to the email account using the App Password
        server.login(sender_email, app_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
