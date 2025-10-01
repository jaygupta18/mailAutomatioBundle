from __future__ import print_function
import os.path
import base64
import re
from email.mime.text import MIMEText
from openai_reply import generate_reply
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(to, subject, message_text):
    
    message = MIMEText(message_text)
    print(message)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        sent_msg = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"📤 Reply sent! Message ID: {sent_msg['id']}")
    except Exception as error:
        print(f"❌ An error occurred while sending the message: {error}")
               
def run_assistant(max_emails=10, reply_style='professional', custom_prompt=''):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    print(f"🔧 Settings: Processing {max_emails} emails with {reply_style} style")
    if custom_prompt:
        print(f"🔧 Custom prompt: {custom_prompt[:100]}...")
  
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread", maxResults=max_emails).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No unread messages.")
        return

    for msg_obj in messages:
        msg = service.users().messages().get(userId='me', id=msg_obj['id'], format='full').execute()
        
        # Get full email content
        email_content = ""
        if 'payload' in msg and 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    email_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        else:
            
            email_content = msg.get('snippet', '')

        from_header = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'From')
        match = re.search(r'<(.+?)>', from_header)
        sender_email = match.group(1) if match else from_header

        subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), "Re:")

        print(f"\n📨 From: {sender_email}")
        print(f"📌 Subject: {subject}")
        print(f"📄 Message: {email_content[:200]}...")

        # Generate AI reply with full context and settings
        context = f"Subject: {subject}\n\nEmail Content:\n{email_content}"
        reply_text = generate_reply(context, reply_style=reply_style, custom_prompt=custom_prompt)
        print(f"\n🤖 AI Reply:\n{reply_text}")

        # Compose and send the message
        reply_msg = create_message(sender_email, f"Re: {subject}", reply_text)
        send_message(service, 'me', reply_msg)

        # Mark the email as read
        service.users().messages().modify(userId='me', id=msg_obj['id'], body={'removeLabelIds': ['UNREAD']}).execute()
        
if __name__ == '__main__':
    run_assistant()
