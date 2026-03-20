import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser

# ----------------- Initialize Text-to-Speech -----------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# ----------------- Wish Based on Time -----------------
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! I am Jarvis, Naveed. How can I help you?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! I am Jarvis, Naveed. How can I help you?")
    else:
        speak("Good Evening! I am Jarvis, Naveed. How can I help you?")

# ----------------- Take Voice Command -----------------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Error:", e)
        return "None"
    return query.lower()

# ----------------- Main Jarvis Logic -----------------
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if query == "none":
            continue

        # Wikipedia Bio
        if 'wikipedia' in query or 'bio' in query:
            query = query.replace("wikipedia", "")
            query = query.replace("bio", "")
            query = query.replace("according to", "")
            query = query.strip()
            try:
                results = wikipedia.summary(query, sentences=5)
                print("\n--- Wikipedia Bio ---")
                print(results)
                print("--------------------\n")
                speak("According to Wikipedia, here is the information.")
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("Your query is ambiguous, please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find any page for your query.")
            except Exception as e:
                print("Wikipedia Error:", e)
                speak("Sorry, I am unable to fetch results right now.")

        # Open YouTube
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # Open Google
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # Search on Google
        elif 'search' in query:
            search_term = query.replace("search", "").strip()
            speak(f"Searching {search_term} on Google")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")

        # Who are you
        elif 'who are you' in query:
            speak("I am Jarvis, an AI assistant created by Naveed.")

        # Exit Jarvis
        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye Sir, have a nice day!")
            break

        # Fallback for unknown queries
        else:
            speak("I am not sure about that. I can search it on Google if you want.")
            webbrowser.open(f"https://www.google.com/search?q={query}")