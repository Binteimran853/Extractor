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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)


    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


    
from base64 import urlsafe_b64decode
import re

def get_latest_code(service, user_input):
    query = f'from:info@account.netflix.com to:{user_input} subject:"Your Netflix temporary access code" label:unread in:inbox newer_than:5h'

    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return None, None

    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    payload = msg['payload']
    parts = payload.get('parts', [])
    plain_body = None
    html_body = None

    if parts:
        for part in parts:
            if part['mimeType'] == 'text/html':
                html_body = part['body'].get('data')
            elif part['mimeType'] == 'text/plain':
                plain_body = part['body'].get('data')
    else:
        # Single part email
        if payload['mimeType'] == 'text/html':
            html_body = payload['body'].get('data')
        elif payload['mimeType'] == 'text/plain':
            plain_body = payload['body'].get('data')

    if html_body:
        html_body_decoded = urlsafe_b64decode(html_body).decode('utf-8')
    else:
        html_body_decoded = ''

    if plain_body:
        plain_body_decoded = urlsafe_b64decode(plain_body).decode('utf-8')
    else:
        plain_body_decoded = ''

    # Extract OTP from plain text body (or HTML body fallback)
    match = re.search(r'\b\d{6}\b', plain_body_decoded)
    if not match:
        match = re.search(r'\b\d{6}\b', html_body_decoded)

    otp = match.group(0) if match else None

    return otp, html_body_decoded
