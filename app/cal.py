import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TOKEN_LOCATION = "app/credentials/token.json"
CREDENTIALS_LOCATION = "app/credentials/credentials.json"


def getEventsOfToday() -> list((str, str)):
 
    creds = Credentials.from_authorized_user_file(TOKEN_LOCATION, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
           CREDENTIALS_LOCATION, SCOPES
        )
        # creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(TOKEN_LOCATION, "w") as token:
      token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = (datetime.date.today() + datetime.timedelta(days=0)).isoformat() + "T00:00:00.0" + "Z"  # 'Z' indicates UTC time
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat() + "T00:00:00.0" + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                timeMax=tomorrow,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return []

        events_of_today = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            events_of_today.append((start, event["summary"]))
        return events_of_today

    except HttpError as error:
        return [("error", "HTTP-error:" + error)]


if __name__ == "__main__":
    print(getEventsOfToday())