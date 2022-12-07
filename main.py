import smtplib
import os
from dotenv import load_dotenv
import datetime as dt
import pandas as pd
import random

load_dotenv()

now = dt.datetime.now()
today_month = now.month
today_day = now.day
today = (today_month, today_day)
letters = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]

my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_PASSWORD")
to_address = os.getenv("TO_ADDRESS")
email_smtp = "smtp.gmail.com"

df = pd.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in df.iterrows()}
if today in birthdays_dict:
    random_letter = random.choice(letters)
    birthday_name = birthdays_dict[today]["name"].title()
    with open(f"./letter_templates/{random_letter}") as data_file:
        letter_content = data_file.read()
        letter_content = letter_content.replace("[NAME]", birthday_name)

    with smtplib.SMTP(email_smtp, port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=to_address,
                            msg=f"Subject:Happy Birthday!!\n\n{letter_content}")
