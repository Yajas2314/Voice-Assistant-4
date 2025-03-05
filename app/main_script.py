from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from gtts import gTTS
import os
import requests
import random


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running on Render!"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Get Render's port
    print(f"🟢 Starting Flask on port {port}...")  # Debugging log
    app.run(host="0.0.0.0", port=port, debug=False)
    gunicorn main:app --bind 0.0.0.0:$PORT

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3") 

# Weather API Key
WEATHER_API_KEY = "089cb559edf9127ca22ca63afa575f8c"

def speak(text):
    engine.say(text)
    engine.runAndWait()
    return text

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("main"):
            weather_desc = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."
        return "Sorry, I couldn't fetch weather for that location."
    except:
        return "Error fetching weather data."

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fish wearing a bowtie? So-fish-ticated!",
        "What do you call a fake noodle? An impasta!"
    ]
    return random.choice(jokes)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    command = data.get("command", "").lower()

    if "weather" in command:
        city = command.split("in")[-1].strip() if "in" in command else "your city"
        response = get_weather(city)

    elif "joke" in command:
        response = tell_joke()

    elif command in ["exit", "quit", "bye"]:
        response = "Goodbye! Have a great day!"

    else:
        response = "Sorry, I didn't understand that command. Type 'help' for available commands."

    return jsonify({"response": speak(response)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
