#read https://pypi.org/project/SpeechRecognition/
# https://pypi.org/project/PyAudio/
# https://pypi.org/project/pywhatkit/
# https://pypi.org/project/wikipedia/
# https://pypi.org/project/pyjokes/

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  # Set timeout and phrase time limit
            command = listener.recognize_google(voice).lower()
            
            if 'alfred' in command:
                command = command.replace('alfred', '').strip()
                print('Recognized command:', command)
                return command
            else:
                print('Keyword "Alfred" not detected.')

    except sr.UnknownValueError:
        print('Speech Recognition could not understand audio.')
    except sr.RequestError as e:
        print(f'Speech Recognition request failed: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

    return None

def run_alexa():
    while True:
        command = take_command()

        if command:
            if 'play' in command:
                song = command.replace('play', '').strip()
                talk('Playing ' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + current_time)
            elif 'who is' in command:
                person = command.replace('who is', '').strip()
                try:
                    info = wikipedia.summary(person, sentences=1)
                    print(info)
                    talk(info)
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"Ambiguous search term: {e}")
                    talk(f"I found multiple results for {person}. Please be more specific.")
                except wikipedia.exceptions.PageError as e:
                    print(f"Could not find information about {person}: {e}")
                    talk(f"I couldn't find information about {person}.")
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'exit' in command:
                talk('Exiting Alfred.')
                break
            else:
                talk('Please say that again.')

if __name__ == "__main__":
    run_alexa()
