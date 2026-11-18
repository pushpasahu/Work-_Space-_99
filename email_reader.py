import os
from pathlib import Path

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

credential = Path(r"config/credentials.json")
token = Path(r"config/token.json")
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]

# if os.path.exists(Path(credential)):
#     print(True)
creds = None
if token.exists():
    creds = Credentials.from_authorized_user_file(str(token), SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(credential),SCOPES)
        creds = flow.run_local_server(port=0)

    with open(token, "w") as token_file:
        token_file.write(creds.to_json())


gmail_driver = build("gmail","v1",credentials=creds)
query = "from:pushpa.sahu@ap.averydennison.com"
result = gmail_driver.users().messages().list(userId="me", q=query).execute()

messages = result.get("messages",[])
for message in messages:
    msg_id = message["id"]
    msg_data = (gmail_driver.users().messages().get(userId="me", id=msg_id).execute())
    payload = msg_data.get("payload",[])
    headers = payload.get("headers",[])

    subject = next(
        (h["value"] for h in headers if h["name"].lower() == "subject"),""
    )
    print(subject)
    # filename = payload.get("filename")
    # body = payload.get("body",{})
    # attachment_id = body.get("attachmentId")

    # attachment = (gmail_driver.users().messages().attachments().get(userID = "me", messagesId=msg_id, id=attachment_id).execute())

    # gmail_driver.users().messages().modify(
    #     userId="me",
    #     id=msg_id,
    #     body={"removeLabelIds":["UNREAD"]},
    # ).execute()
