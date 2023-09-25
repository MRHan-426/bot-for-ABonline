import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from purchase_bot import *

with open('config.txt', 'r') as file:
    lines = file.readlines()

EMAIL_USER = ""
EMAIL_PASS = ""
MAIL_SERVER = ""
SMTP_SERVER = ""
TO_EMAIL = ""
FROM_EMAIL = ""

for line in lines:
    parts = line.strip().split("=")
    if len(parts) == 2:
        key = parts[0].strip()
        value = parts[1].strip()
        if key == "EMAIL_USER":
            EMAIL_USER = value
        elif key == "EMAIL_PASS":
            EMAIL_PASS = value
        elif key == "MAIL_SERVER":
            MAIL_SERVER = value
        elif key == "SMTP_SERVER":
            SMTP_SERVER = value
        elif key == "TO_EMAIL":
            TO_EMAIL = value
        elif key == "FROM_EMAIL":
            FROM_EMAIL = value

print(EMAIL_USER)
print(EMAIL_PASS)
print(MAIL_SERVER)
print(SMTP_SERVER)
print(TO_EMAIL)
print(FROM_EMAIL)

def read_latest_email():
    email_user = EMAIL_USER
    email_pass = EMAIL_PASS
    mail_server = MAIL_SERVER
    imap_port = 993

    mail = imaplib.IMAP4_SSL(mail_server, imap_port)
    mail.login(email_user, email_pass)

    mailbox = "INBOX"
    mail.select(mailbox)
    status, email_ids = mail.search(None, "ALL")
    email_id_list = email_ids[0].split()

    if not email_id_list:
        mail.logout()
        return None, None
    latest_email_id = email_id_list[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    subject, encoding = decode_header(email_message["Subject"])[0]
    if encoding:
        subject = subject.decode(encoding)
    else:
        subject = str(subject)

    from_address = email_message.get("From")

    # if email_message.is_multipart():
    #     for part in email_message.walk():
    #         content_type = part.get_content_type()
    #         if content_type == "text/plain":
    #             body = part.get_payload(decode=True).decode()
    #             print("Body:", body)
    #             break
    mail.logout()
    return subject, from_address


def send_email(subject:str, body:str):

    email_user = EMAIL_USER
    email_pass = EMAIL_PASS
    smtp_server = SMTP_SERVER
    smtp_port = 587

    to_email = TO_EMAIL

    message = MIMEMultipart()
    message["From"] = email_user
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, to_email, message.as_string())
        server.quit()
        print("Mail sent successfully")
        return 1
        
    except Exception as e:
        print("Mail sent Failed:", str(e))
        return 0


def delete_latest_email():

    email_user = EMAIL_USER
    email_pass = EMAIL_PASS
    mail_server = MAIL_SERVER
    imap_port = 993

    mail = imaplib.IMAP4_SSL(mail_server, imap_port)
    mail.login(email_user, email_pass)
    mailbox = "INBOX"
    mail.select(mailbox)
    status, email_ids = mail.search(None, "ALL")
    email_id_list = email_ids[0].split()

    if email_id_list:
        latest_email_id = email_id_list[-1]
        mail.store(latest_email_id, "+FLAGS", "(\\Deleted)")
        mail.expunge()
        print("Latest email has been deleted")
    mail.logout()


if __name__ == '__main__':
    while(1):
        time.sleep(2)
        subject, from_address = read_latest_email()
        print(from_address)
        if from_address == FROM_EMAIL:
            if subject == "Regular" or subject == "regular":
                print("start regular purchase")
                delete_latest_email()
                success = send_email("Regular purchase Start", body="")
                pBot = purchaseBot()
                pBot.mouse_move((794,23))
                pBot.mouse_click()
                time.sleep(1)
                for i in ACCOUNT_LIST[:5]:
                    print(i)
                    pBot.regular_purchase(i)
                    time.sleep(3)
                print("regular purchase end")
                success = send_email("Regular purchase finished", body="")

            elif subject == "order":
                print("start buy order")
                delete_latest_email()
                success = send_email("Buy Order Start", body="")
                pBot = purchaseBot()
                pBot.mouse_move((794,23))
                pBot.mouse_click()
                time.sleep(1)
                for i in ACCOUNT_LIST[:5]:
                    print(i)
                    pBot.purchase_and_create_buy_order(i)
                    time.sleep(3)
                print("Buy Order end")
                success = send_email("Buy order completed", body="")
        else:
            print("waiting for operations")
            pass