import pandas as pd
import random
from datetime import datetime, timedelta

# ----------- Configurable Lists -----------

companies = [
    ("LinkedIn", "linkedin.com"),
    ("Yahoo", "yahoo.com"),
    ("Adobe", "adobe.com"),
    ("Canva", "canva.com"),
    ("Twitter", "twitter.com"),
    ("Facebook", "facebook.com"),
    ("Dropbox", "dropbox.com"),
    ("MySpace", "myspace.com"),
    ("Marriott", "marriott.com"),
    ("Equifax", "equifax.com")
]

attack_types = [
    "Credential Stuffing",
    "Phishing",
    "Database Leak",
    "API Exploit",
    "Social Engineering",
    "Unauthorized Access",
    "Web Vulnerability",
    "Insider Leak"
]

data_types = [
    "Emails+Passwords",
    "Emails+Phone Numbers",
    "Usernames+Passwords",
    "Personal Information",
    "Public Profile Data",
    "Security Questions"
]

names = ["admin", "user", "support", "contact", "employee", "dev", "security", "info"]

# ----------- Helper Functions -----------

def random_date():
    start = datetime(2013, 1, 1)
    end = datetime(2024, 12, 31)
    return start + timedelta(days=random.randint(0, (end-start).days))

def generate_password_hint():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "***" + "".join(random.choice(chars) for _ in range(3))

# ----------- Generate Records -----------

records = []

for _ in range(200):   # You can increase this number later
    company, domain = random.choice(companies)

    email_prefix = random.choice(names)
    email = f"{email_prefix}@{domain}"

    breach_date = random_date().strftime("%Y-%m-%d")
    attack = random.choice(attack_types)
    exposed_data = random.choice(data_types)

    password_exposed = random.choice(["Yes", "No"])

    if password_exposed == "Yes":
        password_hint = generate_password_hint()
    else:
        password_hint = "Not Available"

    records.append([
        email,
        domain,
        company,
        breach_date,
        attack,
        exposed_data,
        password_hint,
        password_exposed
    ])

# ----------- Save Dataset -----------

columns = [
    "email",
    "domain",
    "breach",
    "breach_date",
    "attack_type",
    "data_exposed",
    "password_hint",
    "password_exposed"
]

df = pd.DataFrame(records, columns=columns)

df.to_csv("data/breaches.csv", index=False)

print("Dataset generated successfully with", len(df), "records.")