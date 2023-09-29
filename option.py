import speech_recognition as sr
import os
import pyttsx3

def speak(text):
    engine.say(text)
    engine.runAndWait()

# set up the speech recognition object
r = sr.Recognizer()

# Text-to-speech setup
engine = pyttsx3.init()

# define the function to recognize speech input
def recognize_speech():
    with sr.Microphone() as source:
        speak("Hello I'm here to help you write mail")
        speak("speak send to send mail if not then")
        speak("speak read to read mail")
        audio = r.listen(source)

    try:
        # recognize speech using Google Speech Recognition
        command = r.recognize_google(audio)

        # check if the user wants to send or read email
        if "send" in command.lower():
            os.system("python sendmailfinal.py")
        elif "read" in command.lower():
            os.system("python readinbox.py")
        else:
            speak("Sorry, I didn't understand that. Please try again.")

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Please try again.")
    except sr.RequestError as e:
        speak("Could not request results from Google Speech Recognition service; {0}".format(e))

# run the function to recognize speech input
recognize_speech()
