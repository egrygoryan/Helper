import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]


def authorize():
  credentials = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      credentials.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      credentials = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(credentials.to_json())

  return credentials

def add_task(service, title: str, notes: str=None):
  body = {"title": title}
  if notes:
    body["notes"] = notes
  
  created_task = service.tasks().insert(tasklist="@default", body=body).execute()
  return created_task
  
def run(title: str, notes: str=None):
  try:
    credentials = authorize()
    service = build("tasks", "v1", credentials=credentials)
    created_task = add_task(service, title, notes)
    
    return created_task
  except HttpError as err:
    print(err)
