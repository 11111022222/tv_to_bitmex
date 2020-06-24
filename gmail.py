import bitmex_strategies as bmx #correspond au fichier de gestion des stratégies
import datetime, os.path, pickle, pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PICKLE = '/root/trading_automated_strategies/bitmex_strategies/gmail_ressources/token.pickle' # à remplacer par le chemin vers votre token.pickle
TOKEN_CREDENTIALS = '/root/trading_automated_strategies/bitmex_strategies/gmail_ressources/credentials.json' #à remplacer par le chemin vers votre credentials.json
MAIL_TEXT = "Votre alerte" #texte minimal permettant d'identifier un email provenant de tradingview et correspondant à une alerte
def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(TOKEN_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)
#datetime
    utc=pytz.UTC
    now = datetime.datetime.now()    
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
delta=datetime.timedelta(minutes = 1,seconds = 30)
print(">> Current date : %s " % now)
    if messages:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            if(MAIL_TEXT in msg['snippet']):
                internalDate = datetime.datetime.fromtimestamp(int(msg['internalDate'])/1000).strftime('%c')
                internalDate = datetime.datetime.strptime(internalDate, '%a %b %d %H:%M:%S %Y')
                #if a recent tradingview mail arrived
                if((now - internalDate) < delta):
                    #we send the snippet to the bitmex_algorithm
                    email_snippet = str(msg['snippet'])
                    bmx.call_strategy(email_snippet)
                    break
                break
if __name__ == '__main__':
    main()
