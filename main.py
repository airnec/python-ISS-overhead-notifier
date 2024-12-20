from datetime import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MY_LAT = 41.008240
MY_LONG = 28.978359

def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    position = data["iss_position"]
    iss_lat = float(position["latitude"])
    iss_long = float(position["longitude"])

    if ((MY_LAT + 5) <= iss_lat <= (MY_LAT + 5)) and ((MY_LONG + 5) <= iss_long <= (MY_LAT + 5)):
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour <= sunrise or time_now.hour >= sunset:
        return True

# SENDING EMAIL
# ------------------------------------------------------------------------
# Email Configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # For TLS
email_address = "example@example.com"
email_password = "password"  # Use app password if 2FA is enabled

# Recipients
to_emails = ["example@example.com"]  # Main recipients
# cc_emails = ["cc1@example.com", "cc2@example.com"]  # CC recipients
# bcc_emails = ["bcc1@example.com", "bcc2@example.com"]  # BCC recipients

# Create Email
subject = "Heads Up! ISS is passing over!"
body = "Hey! ISS is passing over your location. Look up how amazing it is there!"

message = MIMEMultipart()
message["From"] = email_address
message["To"] = ", ".join(to_emails)  # Visible recipients
# message["Cc"] = ", ".join(cc_emails)  # Visible CC recipients
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

if is_iss_overhead() and is_night():
    try:
        # Connect to SMTP Server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade to secure connection
        server.login(email_address, email_password)
        server.sendmail(email_address, to_emails, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()