import os
import schedule
import time
import requests

# Carrega variáveis do Render
from dotenv import load_dotenv
load_dotenv()

# Twilio / WhatsApp
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
FROM_NUMBER = "whatsapp:+14155238886"  # Número fixo do Twilio
TO_NUMBER = os.getenv("TO_NUMBER")     # Seu WhatsApp pessoal
GEMINI_KEY = os.getenv("GEMINI_KEY")


# Função para gerar frase diária usando Gemini
def gerar_frase_diaria():
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY
    payload = {
        "contents": [{"parts": [{"text": "Me indique um livro para eu ler hoje."}]}]
    }

    r = requests.post(url, json=payload)
    resposta = r.json()
    return resposta["candidates"][0]["content"]["parts"][0]["text"]


# Enviar mensagem pelo WhatsApp
def enviar_mensagem():
    frase = gerar_frase_diaria()

    r = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
        data={
            "From": FROM_NUMBER,
            "To": TO_NUMBER,
            "Body": frase
        },
        auth=(TWILIO_SID, TWILIO_TOKEN)
    )

    print("Mensagem enviada:", frase)


# Agenda para enviar todos os dias às 08:00
schedule.every().day.at("08:00").do(enviar_mensagem)

print("Automação ativa! Aguardando horário...")

while True:
    schedule.run_pending()
    time.sleep(60)
