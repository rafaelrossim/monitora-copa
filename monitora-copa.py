import requests, json, os
from datetime import datetime
from json import JSONDecodeError

# caso queria usar uma API free do WhatsApp
    # docs - https://pypi.org/project/pywhatkit/

# WhatsApp API oficial
    # docs - https://benalexkeen.com/send-whatsapp-messages-using-python/
    # docs - https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
    # docs - https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#text-messages

# obtendo data
d_today = datetime.today()
d_today = d_today.strftime("%d-%m-%Y")

# obtendo variáveis
tel = "5511999999999" # coloque o número de telefoe que receberá as atualizações
time1 = "digite_time1"
time2 = "digite_time2"


def send_wtp(tel, msg):
    url = "https://graph.facebook.com/v15.0/number_id_api_whatsapp/messages"
    
    payload = json.dumps({
    "messaging_product": "whatsapp",
    "to": tel, 
    "type": "text", 
    "text": {
        "preview_url": False,
        "body": msg
        }
    })
    
    headers = {
        'Authorization': os.getenv("token_wtp"), # coloque a chave do WhatsAPP API
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    res = json.loads(response.text)
    return res

def get_match_data():
    try:  
        match = requests.get(url="https://temporeal.lance.com.br/storage/matches/copa-do-mundo-2022-"+str(d_today)+"-"+str(time1)+"x"+str(time2)+".json").json()   
    except JSONDecodeError:
        match = requests.get(url="https://temporeal.lance.com.br/storage/matches/copa-do-mundo-2022-"+str(d_today)+"-"+str(time2)+"x"+str(time1)+".json").json()
    return match


last_update = None                                                                                    
while True:
    match_data = get_match_data()
    
    narrations = match_data["match"]["narrations"]
    try:
        last_narration = narrations[len(narrations)-1]
        last_narration_time = datetime.strptime(last_narration["created_at"], "%Y-%m-%dT%H:%M:%S.000000Z")
        
        if (not last_update) or (last_narration_time > last_update):
            last_update = last_narration_time
            last_narration_moment = narrations[len(narrations)-1]["moment"]
            last_narration_text = narrations[len(narrations)-1]["text"]
            
            if last_narration_moment == None:
                result = "News - " + str(last_narration_text)
                send_wtp(tel, result)
                print(result)

            else:
                result = str(last_narration_moment) + "mins - " + str(last_narration_text)
                send_wtp(tel, result)
                print(result)
                    
    except IndexError:
        print("Partida não iniciada, favor tente mais tarde!")
        break