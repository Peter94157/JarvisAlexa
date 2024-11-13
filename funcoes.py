import requests
import json
from datetime import datetime, timedelta


#IMPORTAÇÕES API GOOGLE SHEETS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class Lembrete():

    from datetime import datetime, timedelta
import requests
import json


class Lembrete:
    
    def ConsultarLembretes(self, acess_token):
        url = 'https://api.amazonalexa.com/v1/alerts/reminders'

        headers = {
            'Authorization': f'Bearer {acess_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                lembretes = response.json()
                print("Lembretes existentes:")
                print(json.dumps(lembretes, indent=4, ensure_ascii=False))
                return lembretes
            else:
                print(f"Erro ao consultar lembretes: {response.status_code}")
                print("Resposta:", response.text)
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a resposta JSON: {e}")
        
        return None

    def CriandoLembrete(self, acess_token, mensagem, duracaop, recurrence=None):
        print("Access Token:")
        print(acess_token)

        # Validar e processar `duracaop`
        try:
            horas, minutos = map(int, duracaop.split(':'))
            duracao = horas * 60 + minutos  # Resultado em minutos
        except ValueError:
            raise ValueError("O valor de 'duracaop' deve estar no formato 'HH:MM'.")

        # Calcular o horário de agendamento
        now = datetime.utcnow() + timedelta(hours=1, minutes=26)
        scheduled_time = (now + timedelta(minutes=duracao)).strftime("%Y-%m-%dT%H:%M:%S")

        mensagem = mensagem or "Tomar remédio"  # Mensagem padrão
        
        url = 'https://api.amazonalexa.com/v1/alerts/reminders'
        data = {
            "requestTime": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "trigger": {
                "type": "SCHEDULED_ABSOLUTE",
                "scheduledTime": scheduled_time
            },
            "alertInfo": {
                "spokenInfo": {
                    "content": [{
                        "locale": "pt-BR",
                        "text": mensagem,
                        "ssml": f"<speak>{mensagem}</speak>"
                    }]
                }
            },
            "pushNotification": {
                "status": "ENABLED"
            }
        }

        # Adicionar recorrência se especificada
        if recurrence:
            data["trigger"]["recurrence"] = {
                "freq": recurrence.get("freq", "DAILY"),
                "byDay": recurrence.get("byDay", []),
                "interval": recurrence.get("interval", 1)
            }

        headers = {
            'Authorization': f'Bearer {acess_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print("Lembrete criado com sucesso!")
                print(response.json())
            elif response.status_code == 204:
                print("Lembrete criado, mas sem conteúdo na resposta.")
            else:
                print(f"Erro na criação do lembrete: {response.status_code}")
                print("Resposta:", response.text)
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a resposta JSON: {e}")
        
        return response.status_code



class Driver():

    def __init__(self):
        # self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        self.SAMPLE_SPREADSHEET_ID = "1BSGdhMDpHn06MyNTnRXDykIAUYt-LX3nu68WHHDPOlk"
        # self.SAMPLE_RANGE_NAME = "RegistroRemedio!b2:b"

    

    def Credenciais(self):
        credentials_path = r"token.json"
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes)
        return creds

    def ConsultaRemedio(self):
        creds = self.Credenciais()
        try:
            #Lê as informações do Google Sheets
            service = build("sheets", "v4", credentials=creds)
            
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="B:B")
                .execute()
            )
            print(result['values'])
            return result['values'][0][0]
        # valores_add = [
        #     ["Diporona","1ml"]
        #]
        #Adicionar informações dentro da planilha
        #     result = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,
        #                                   range = "B2", valueInputOption = "USER_ENTERED",
        #                                   body = {"values": valores_add}).execute()
        except HttpError as err:
            print(err)


    def cadastroRemedio(self,valores_add):
        if not valores_add:
            return
        creds = self.Credenciais()
        try:
            service = build("sheets","v4", credentials=creds)
            
            sheet = service.spreadsheets()
            result = sheet.values().update(spreadsheetId = self.SAMPLE_SPREADSHEET_ID,range = "g1", valueInputOption = "USER_ENTERED", body = {"values":valores_add}).execute()
        
        except HttpError as err:
            print(err)
    
    
