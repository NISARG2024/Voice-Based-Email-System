import base64
import os.path
import pickle
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import speech_recognition as sr
import pyttsx3

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech recognition setup
r = sr.Recognizer()

# Text-to-speech setup
engine = pyttsx3.init()


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'client_secret_516696085222-ji3dro8iu4gtte873d5hftfqm45dj6gp.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to get the user's email messages.
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])

    if not messages:
        speak('No unread messages found.')
    else:
        print((f"Total unread messages: {len(messages)}"))
        speak(f"Total unread messages: {len(messages)}")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            message_data = msg['payload']['headers']
            for header in message_data:
                if header['name'] == 'From':
                    print(f"From: {header['value']}")
                    speak(f"From: {header['value']}")

                if header['name'] == 'Subject':
                    print(f"Subject: {header['value']}")
                    speak(f"Subject: {header['value']}")

                if header['name'] == 'Date':
                    print(f"Date: {header['value']}")
                    speak(f"Date: {header['value']}")

if __name__ == '__main__':
    main()
