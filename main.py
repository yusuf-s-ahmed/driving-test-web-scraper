import requests
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

url = "https://lidt.co.uk/fast-track-booking"
html = requests.get(url).text



pattern = re.compile(
    r"(Herne|Wood Green|Loughton|Belvedere|Erith|Sidcup|Bromley).*?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{2}:\d{2}",
    re.DOTALL
)


matches = pattern.findall(html)
target_centres = ["Erith", "Sidcup", "Bromley", "Belvedere"]
target_months = ["Feb", "March"]


# Email settings

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAILS = os.getenv("TO_EMAILS").split(",")  # Convert to list

def send_email(centre, day):
    subject = f"Driving Test Slot Found at {centre}"
    body = f"A slot has been found at {centre} on {day}.\n\nVisit the site to book: {url}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(TO_EMAILS)  # display list of recipients
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAILS, msg.as_string())  # send to all
        print(f"Email sent for {centre} on {day} to {len(TO_EMAILS)} people")
    except Exception as e:
        print(f"Failed to send email: {e}")


sent_slots = set()  # to track & avoid duplicate emails

sent_slots = set()

if not matches:
    print("No slots found")
else:
    for centre, day in matches:
        slot_key = f"{centre}-{day}"

        if centre in target_centres and day in target_months:
            if slot_key not in sent_slots:
                print(f"✓ Slot(s) found at {centre} on {day}")
                send_email(centre, day)
                sent_slots.add(slot_key)
            else:
                print(f"Skipping duplicate slot at {centre} on {day}")
        else:
            print(f"Skipping {centre} on {day}")
