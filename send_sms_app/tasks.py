from celery import shared_task
import requests
import time
import dotenv

@shared_task
def get_token(url):
    payload = {
        "grant_type": "client_credentials"
    }
    headers = {
        "Authorization": "AUTHORIZATION",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    rq = requests.post(url, data=payload, headers=headers)
    rq_json = rq.json()
    return rq_json["access_token"]




@shared_task
def send_mass_sms_task(phone_list, content_list, access_token):


    url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B2250707830932/requests"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    for phone in phone_list:
        data = {
            "outboundSMSMessageRequest": {
		        "address": f"tel:+225{phone}",
		        "senderAddress":"tel:+2250707830932",
                "senderName": "MUPEPPBO",
		        "outboundSMSTextMessage": {
			        "message": f"{content_list}"
                }
            }()
		}
        rq = requests.post(url=url, json=data, headers=headers)
        print(f"Contenu de la reponse : {rq.json()}")
        time.sleep(0.2)