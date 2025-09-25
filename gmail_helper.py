import base64
from email.mime.text import MIMEText



def read_recent_unread_emails_ascending(service):
    def fetch_recent_unread_messages():
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread newer_than:7d",
            maxResults=500  
        ).execute()
        return results.get('messages', [])

    def get_email_details(messages):
        detailed_emails = []

        for msg in messages:
            msg_id = msg['id']
            msg_detail = service.users().messages().get(userId='me', id=msg_id).execute()

            headers = msg_detail['payload']['headers']
            subject = [h['value'] for h in headers if h['name'] == 'Subject']
            sender = [h['value'] for h in headers if h['name'] == 'From']
            snippet = msg_detail.get('snippet', '')
            timestamp = int(msg_detail.get('internalDate', '0'))

            detailed_emails.append({
                'id': msg_id,
                'subject': subject[0] if subject else '',
                'from': sender[0] if sender else '',
                'snippet': snippet,
                'timestamp': timestamp
            })

        
        return sorted(detailed_emails, key=lambda x: x['timestamp'])

    def mark_as_read(emails):
        for email in emails:
            service.users().messages().modify(
                userId='me',
                id=email['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()

    messages = fetch_recent_unread_messages()
    sorted_emails = get_email_details(messages)
    mark_as_read(sorted_emails)

    return sorted_emails


def send_reply(service, to_email, subject, body_text):
    message = MIMEText(body_text)
    message['to'] = to_email
    message['subject'] = f"Re: {subject}"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}
    send = service.users().messages().send(userId='me', body=message).execute()
    return send


