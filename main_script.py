import subprocess
import sys

def install_modules():
    modules = [
        'SpeechRecognition',
        'requests',
        'pyjokes',
        'pywhatkit'
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



import streamlit as st
import requests
import math
import pyjokes
import pywhatkit

OPENWEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

grocery_list = []

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        data = requests.get(url).json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"The temperature in {city} is {temp}°C with {desc}."
    except:
        return "Sorry, I couldn't fetch the weather."

def calculate(expression):
    try:
        result = eval(expression)
        return f"The result is {result}"
    except Exception:
        return "Error in calculation."

def log_antilog(command):
    if "log" in command:
        try:
            num = float(command.split()[-1])
            return f"The log of {num} is {math.log10(num)}"
        except:
            return "Invalid number for log."
    elif "antilog" in command:
        try:
            num = float(command.split()[-1])
            return f"The antilog of {num} is {10 ** num}"
        except:
            return "Invalid number for antilog."
    return ""

def play_song_youtube(song):
    # Just return the URL to open in browser
    return f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"

def process_command(command):
    response = ""
    if "play" in command and ("music" in command or "song" in command or "play" in command):
        song = command.replace("play", "").strip()
        url = play_song_youtube(song)
        response = f"Playing {song} on YouTube: [Click here]({url})"

    elif "weather in" in command:
        city = command.split("in")[-1].strip()
        response = get_weather(city)

    elif "calculate" in command:
        expression = command.replace("calculate", "").strip()
        response = calculate(expression)

    elif "log" in command or "antilog" in command:
        response = log_antilog(command)

    elif "joke" in command:
        response = pyjokes.get_joke()

    elif "add to grocery" in command:
        item = command.replace("add to grocery", "").strip()
        grocery_list.append(item)
        response = f"Added {item} to grocery list."

    elif "show grocery list" in command:
        if grocery_list:
            response = "Your grocery list: " + ", ".join(grocery_list)
        else:
            response = "Your grocery list is empty."

    elif "exit" in command or "stop" in command:
        response = "Goodbye! Refresh page to start again."

    else:
        response = "Sorry, I didn't understand that."

    return response

st.title("Zephyr - Your AI Assistant (Web Version)")

command = st.text_input("Type your command here:")

if st.button("Send") and command:
    response = process_command(command.lower())
    st.markdown(response)
