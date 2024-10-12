import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source,timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print(command)
                return command
    except Exception as e:
        print(f"Error: {e}")  # Print the error for debugging
    return ""  # Return empty string if there was an error

def run_alexa():
    command = take_command()
    if command:  # Proceed only if the command is not empty
        print(command)
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'stop' in command:
            talk('Exiting...')
            return False  # Return False to stop the loop
        else:
            talk('Please say the command again.')
    else:
        talk('I did not catch that. Please repeat your command.')
    return True  # Return True to continue the loop

while True:
    if not run_alexa():
        break  # Exit the loop if 'stop' is commanded

