import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_SECRET_FILE = 'client_secret_516696085222-ji3dro8iu4gtte873d5hftfqm45dj6gp.apps.googleusercontent.com.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

# create a recognizer object
r = sr.Recognizer()

# function to recognize speech input
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text.replace(" "," ")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# create Gmail service
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# ask for recipient
tts = gTTS(text="Who would you like to send the email to?", lang="en")
tts.save("recipient.mp3")
playsound("recipient.mp3")
recipientm= recognize_speech().replace(" ","")
recipient = recipientm + "@gmail.com"
mimeMessage = MIMEMultipart()
#mimeMessage['to'] = "hmp2628@gmail.com"
mimeMessage['to'] = recipient


# ask for subject
print("What should the subject of the email be?")
tts = gTTS(text="What should the subject of the email be?", lang="en")
tts.save("subject.mp3")
playsound("subject.mp3")
subject = recognize_speech()
mimeMessage['subject'] = subject

# ask for email body
tts = gTTS(text="What should the body of the email say?", lang="en")
tts.save("body.mp3")
playsound("body.mp3")
emailMsg = recognize_speech()
mimeMessage.attach(MIMEText(emailMsg, 'plain'))

# create raw message string
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

# send email
message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)

# list inbox messages
result = service.users().messages().list(userId='me', q='in:inbox').execute()
messages = result.get('messages', [])
