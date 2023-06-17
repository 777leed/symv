import requests
import openai
import time
import json

### this is working perfectly but only for one user

# def simpleGetMessages():
#     url = "https://api.ultramsg.com/instance50713/chats/messages"
#     querystring = {
#         "token": "8un7kff35gthpm1v",
#         "chatId": "212672916435@c.us",
#         "limit": 1
#     }
#     headers = {'content-type': 'application/x-www-form-urlencoded'}
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     messages = json.loads(response.text)
#     second_message_body = messages[0]["body"]
#     fromMe = messages[0]["fromMe"]
#     if(fromMe == False):
#         return second_message_body
#     else:
#         return "not from user"

def advancedGetMessages():
    url = "https://api.ultramsg.com/instance50713/chats/messages"
    querystring = {
        "token": "8un7kff35gthpm1v",
        "chatId": "212672916435@c.us",
        "limit": 1
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, headers=headers, params=querystring)
    messages = json.loads(response.text)
    second_message_body = messages[0]["body"]
    fromMe = messages[0]["fromMe"]
    print("Establishing...")

    if(fromMe == False):
        number_raw = messages[0]["from"]
        number_parts = number_raw.split("@")
        number = number_parts[0]
        print("from: +", number)
        print("Waiting For CHAT GPT...")
        answer = get_reply(second_message_body)
        print("Answer Received...")
        print("Sending To User")
        sendMessages(answer,f"+{number}")
        clearMessages()
        print("Reply Sent!...")
        return second_message_body
        
    else:
        return "Still Waiting...\n---"


def clearMessages():

    url = "https://api.ultramsg.com/instance50713/chats/clearMessages"
    payload = "token=8un7kff35gthpm1v&chatId=212672916435@c.us"
    payload = payload.encode('utf8').decode('iso-8859-1')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    requests.request("POST", url, data=payload, headers=headers)
    

def sendMessages(message,number):
    try:
        url = "https://api.ultramsg.com/instance50713/messages/chat"
        payload = f"token=8un7kff35gthpm1v&to={number}&body={message}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            print("Message Sent~!")
    except:
        print("There was an error")

def getStats():
    url = "https://api.ultramsg.com/instance50713/messages/statistics"
    querystring = {
        "token": "8un7kff35gthpm1v"
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text


def get_reply(qst):
        openai.api_key = "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"
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": qst}
        ]
        )
        return completion.choices[0].message["content"]

def main():
    while True:
       print(advancedGetMessages())
       time.sleep(2)


main()
