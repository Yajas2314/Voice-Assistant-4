import subprocess
import sys

def install_modules():
    modules = [
        'gtts',
        'SpeechRecognition',
        'requests'
    ]
    
    for module in modules:
        try:
            print(f"Installing {module}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                                '--default-timeout=100', module])
            print(f"Successfully installed {module}")
        except Exception as e:
            print(f"Error installing {module}: {e}")

if __name__ == "__main__":
    print("Starting module installation...")
    install_modules()
    print("Installation process completed!")



from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os
import speech_recognition as sr
import requests
import random

app = Flask(__name__)

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Install mpg321 if needed


# Weather API key
WEATHER_API_KEY = "089cb559edf9127ca22ca63afa575f8c"

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()
    return text

def listen():
    """Captures audio and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='en-US')
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def get_weather(city):
    """Fetches weather details for a given city."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            weather_desc = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."
        return "Sorry, I couldn't fetch weather for that location."
    except:
        return "Sorry, there was an error getting the weather information."

def tell_joke():
    """Returns a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fish wearing a bowtie? So-fish-ticated!",
        "What do you call a fake noodle? An impasta!"
    ]
    return random.choice(jokes)

@app.route('/')
def home():
    """Renders the main webpage."""
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    """Handles user commands from the frontend."""
    data = request.json
    user_input = data.get("query", "").lower()

    if "weather" in user_input:
        if "in" in user_input:
            city = user_input.split("in")[-1].strip()
        else:
            return jsonify({"response": "Please specify a city."})
        response_text = get_weather(city)

    elif "joke" in user_input:
        response_text = tell_joke()

    elif "exit" in user_input or "bye" in user_input:
        response_text = "Goodbye! Have a great day!"

    else:
        response_text = "Sorry, I didn't understand that command."

    speak(response_text)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)

