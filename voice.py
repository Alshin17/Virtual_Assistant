import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests

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
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'antony' in command:
                command = command.replace('antony', '')
                print(command)
    except:
        pass
    return command

def get_news():
    try:
        api_key = 'my API key here'  #my api key
        url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
        response = requests.get(url)
        articles = response.json().get('articles', [])
        if articles:
            talk('Here are some top news headlines:')
            for article in articles[:3]:
                talk(article['title'])
        else:
            talk('Sorry, I am unable to fetch news at the moment.')
    except Exception as e:
        print("Error fetching news:", e)
        talk('There was an error fetching the news.')

def analyze_mood(command):
    """Analyze the mood based on the command."""
    if 'happy' in command or 'great' in command or 'good' in command:
        return 'happy'
    elif 'sad' in command or 'bad' in command or 'angry' in command:
        return 'sad'
    else:
        return 'neutral'

def run_antony():
    command = take_command()
    print(command)
    mood = analyze_mood(command)  # Analyze mood based on the command

    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'news' in command:
        get_news()
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'how are you' in command:
        if mood == 'happy':
            talk('I am glad to hear you are happy!')
        elif mood == 'sad':
            talk('I’m sorry to hear that. I’m here for you.')
        else:
            talk('I am feeling great, thank you!')
    else:
        talk('Please say the command again.')

while True:
    run_antony()
