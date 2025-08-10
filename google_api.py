from __future__ import print_function
import re
from base64 import urlsafe_b64decode
from urllib.parse import unquote
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
from bs4 import BeautifulSoup

def get_latest_code(service, user_input):
    query = (
        f'from:info@account.netflix.com to:{user_input} '
        'subject:"Your Netflix temporary access code" '
        'label:unread in:inbox newer_than:15m'
    )
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return  None, []

    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    def get_parts(payload):
        if 'parts' in payload:
            for part in payload['parts']:
                yield from get_parts(part)
        else:
            yield payload

    plain_body_decoded = ''
    html_body_decoded = ''

    for part in get_parts(msg['payload']):
        mimeType = part.get('mimeType')
        data = part['body'].get('data')
        if data:
            decoded = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            if mimeType == 'text/plain':
                plain_body_decoded += decoded
            elif mimeType == 'text/html':
                html_body_decoded += decoded

    # Extract OTP
    match = re.search(r'\b\d{4,8}\b', plain_body_decoded) or re.search(r'\b\d{4,8}\b', html_body_decoded)
    otp = match.group(0) if match else None

    # Extract Netflix verify link
    verify_link = None
    if html_body_decoded:
        soup = BeautifulSoup(html_body_decoded, "html.parser")
        anchors = soup.find_all('a', href=True)

        for a in anchors:
            href = a['href'].strip()

            # Decode Google redirect
            if href.startswith("https://www.google.com/url?q="):
                href = unquote(href.split("q=")[1].split("&")[0])

            # Match the Netflix verification link
            if "/account/travel/verify" in href and "messageGuid=" in href:
                verify_link = href  # keep the whole thing, no slicing
                print("Netflix Verification Link Found:", verify_link)
                break

    return  html_body_decoded, verify_link 