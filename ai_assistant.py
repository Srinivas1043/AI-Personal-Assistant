import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests
import dotenv
import ollama

# Load environment variables
dotenv.load_dotenv()

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture audio input"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        speak("Could not connect to the internet.")
        return ""

def get_time():
    """Get the current time"""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def search_wikipedia(query):
    """Fetch summary from Wikipedia"""
    speak("Searching Wikipedia...")
    result = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia, " + result)

def open_website(command):
    """Open popular websites"""
    if "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")
    else:
        speak("Sorry, I don't recognize that website.")

def get_weather(city):
    """Fetch weather data from OpenWeather API"""
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response["cod"] != 200:
        speak("Sorry, I couldn't fetch the weather information.")
        return

    temp = response["main"]["temp"]
    description = response["weather"][0]["description"]
    speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")

def ask_llama(prompt):
    """Get a response from LLaMA 2 or Mistral"""
    response = ollama.chat(model='mistral', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def ai_assistant():
    """Main function for the AI assistant"""
    speak("Hello! How can I assist you?")
    while True:
        command = listen()

        if "wikipedia" in command:
            query = command.replace("wikipedia", "")
            search_wikipedia(query)

        elif "time" in command:
            get_time()

        elif "open" in command:
            open_website(command)

        elif "weather in" in command:
            city = command.split("weather in")[-1].strip()
            get_weather(city)

        elif "ask" in command or "question" in command:
            speak("What do you want to ask?")
            user_query = listen()
            response = ask_llama(user_query)
            speak(response)

        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            break

if __name__ == "__main__":
    print("Starting AI Assistant...")
    ai_assistant()