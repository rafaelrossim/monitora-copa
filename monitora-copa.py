# WhatsApp API oficial
    # docs - https://benalexkeen.com/send-whatsapp-messages-using-python/
    # docs - https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
    # docs - https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#text-messages

# WhatsApp API não oficial
    # docs - https://pypi.org/project/pywhatkit/

# Telegram API
    # https://core.telegram.org/bots
    # https://www.shellhacks.com/python-send-message-to-telegram
    # https://api.telegram.org/bot5932518359:AAHXElgy8dHULN40ALS5rcE6fjIwfkQaywM/getUpdates


# importando libs
import requests, json, os, time
from datetime import datetime
from json import JSONDecodeError
from unidecode import unidecode

# obtendo data
d_today = datetime.today()
d_today = d_today.strftime("%d-%m-%Y")

# declarando variáveis de contatos
tel = "5511999999999" # telefone para o whatsapp
chatid = ["-9999999999999"] # chatID do telegram (tem que começar com número negativo)

# declarando e tratando nomes dos times para url
time1 = "time1"
time1 = time1.lower()
time1 = time1.replace(" ", "-")
time1 = unidecode(time1)

time2 = "time2"
time2 = time2.lower()
time2 = time2.replace(" ", "-")
time2 = unidecode(time2)


def send_telegram(message, chatid):
    """Função que reaiza o envio de mensagem, utilizando a API Telegram

    Args:
        message (str): Mensagem a ser enviada
        chatid (str): ChatID do contato ou grupo desejado a receber a mensagem
    """

    apiToken = os.getenv("token_tlg") # coloque a chave do Bot Telegram API
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        requests.post(apiURL, json={'chat_id': chatid, 'text': message})
    except Exception as e:
        print(e)
        

def send_wtp(tel, msg):
    """Função que realiza o envio de mensagem, utilizando a API WhatsApp

    Args:
        tel (str): Telefone que receberá a a mensagem
        msg (str): Mensagem a ser enviada

    Returns:
        json: Retorno do status da mensagem
    """
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
    """Função que obtem os dados dos jogos e envia as respectivas mensagens as APIs

    Returns:
        json: Status dos jogos
    """
    try:  
        match = requests.get(url="https://temporeal.lance.com.br/storage/matches/copa-do-mundo-2022-"+str(d_today)+"-"+str(time1)+"x"+str(time2)+".json").json()   
    except JSONDecodeError:
        match = requests.get(url="https://temporeal.lance.com.br/storage/matches/copa-do-mundo-2022-"+str(d_today)+"-"+str(time2)+"x"+str(time1)+".json").json()
    return match


last_update = None                                                                                    
while True:
    match_data = get_match_data()
    
    try:
        narrations = match_data["match"]["narrations"]
        last_narration = narrations[len(narrations)-1]
        last_narration_time = datetime.strptime(last_narration["created_at"], "%Y-%m-%dT%H:%M:%S.000000Z")
        
        if (not last_update) or (last_narration_time > last_update):
            last_update = last_narration_time
            last_narration_moment = narrations[len(narrations)-1]["moment"]
            last_narration_text = narrations[len(narrations)-1]["text"]
            
            if last_narration_moment == None:
                result = "News - " + str(last_narration_text)
                print(result)
                
                for c in chatid:
                    send_telegram(result, c)

            else:
                result = str(last_narration_moment) + "mins - " + str(last_narration_text)
                print(result)
                
                for c in chatid:
                    send_telegram(result, c)
                    
    except IndexError:
        time.sleep(120) # 2mins