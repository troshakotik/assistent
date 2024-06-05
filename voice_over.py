import pyttsx3

def speak(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Optionally, you can adjust properties like voice, rate, and volume
    voices = engine.getProperty('voices')
    print(voices)
    engine.setProperty('voice', voices[1].id)  # Change index to choose a different voice
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()

# Example usage
speak("Hello, how can I assist you today?")
