from celery import shared_task
import requests
import time
import os
from dotenv import load_dotenv


load_dotenv()

@shared_task
def get_token():
    url = os.getenv("TOKEN_URL")
    payload = {
        "grant_type": "client_credentials"
    }
    headers = {
        "Authorization": os.getenv("AUTH_HEADER"),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    rq = requests.post(url, data=payload, headers=headers)
    print(f"Le token est: {rq.json()["access_token"]}")
    return rq.json()["access_token"]




@shared_task
def send_mass_sms_task(phone_list, content_list, access_token):

    url = os.getenv("SEND_SMS_URL")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # print(f"Les données à envoyer: phone list: {phone_list}, content list: {content_list}, access token: {access_token}")
    for phone in phone_list:
        payload = {
            "outboundSMSMessageRequest": {
		        "address": f"tel:+225{phone}",
		        "senderAddress":"tel:+2250707830932",
                "senderName": "MUPEPPBO",
		        "outboundSMSTextMessage": {
			        "message": f"{content_list}"
                }
            }
		}
        rq = requests.post(url=url, json=payload, headers=headers)
        print(f"REQUETE: {rq.text}")
        time.sleep(0.2)