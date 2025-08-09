from __future__ import print_function
import re
from base64 import urlsafe_b64decode

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Gmail API scope for read-only access
SCOPES = ['https://mail.google.com/']
our_email = 'binteimran853@gmail.com'

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


    


def get_latest_code(service, user_input):
    query = f'from:{our_email} to:{user_input} subject:"Your sign-in code" label:unread in:inbox newer_than:15m'
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return None

    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    # Get the body text
    payload = msg['payload']
    parts = payload.get('parts', [])
    body_data = None

    if parts:
        # Sometimes OTP is in multipart -> find text/plain part
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body_data = part['body']['data']
                break
    else:
        # Single part email
        body_data = payload['body'].get('data')

    if not body_data:
        print("No body data found.")
        return None

    body_text = urlsafe_b64decode(body_data).decode('utf-8')

    # Extract OTP (assuming it's 6 digits)
    match = re.search(r'\b\d{6}\b', body_text)
    if match:
        return match.group(0)

    return None

if __name__ == '__main__':
    service = authenticate_gmail()
    user_input = ""
    code = get_latest_code(service, user_input)
    if code:
        print(f"Your verification code is: {code}")
    else:
        print("No code found in recent emails.")
