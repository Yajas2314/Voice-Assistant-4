from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Route to render homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to process voice input
@app.route('/process_voice', methods=['POST'])
def process_voice():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        command = recognizer.recognize_google(audio).lower()
        print("User said:", command)

        # Process voice commands
        if "hello" in command:
            response = "Hello! How can I help you?"
        elif "your name" in command:
            response = "I am your voice assistant."
        elif "time" in command:
            from datetime import datetime
            response = f"The current time is {datetime.now().strftime('%I:%M %p')}"
        elif "exit" in command or "stop" in command:
            response = "Goodbye!"
        else:
            response = "Sorry, I didn't understand that."

        speak(response)
        return jsonify({"response": response})

    except sr.UnknownValueError:
        return jsonify({"response": "Sorry, I couldn't understand."})
    except sr.RequestError:
        return jsonify({"response": "Error with the Speech Recognition API."})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
