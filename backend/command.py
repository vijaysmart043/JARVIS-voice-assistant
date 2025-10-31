import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # Pick a voice safely (fall back to first available)
    try:
        voice_to_use = voices[2].id if len(voices) > 2 else voices[0].id
    except Exception:
        voice_to_use = voices[0].id if voices else None
    if voice_to_use:
        engine.setProperty('voice', voice_to_use)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    eel.receiverText(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        
        
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    try:
        # Handle input message or voice command
        if message is None:
            query = takecommand()  # If no message is passed, listen for voice input
            if not query:
                speak("I didn’t catch that. Please try again.")
                eel.ShowHood()
                return ""  # Ensure Eel gets a return value
            print(query)
            eel.senderText(query)
        else:
            query = message  # If there's a message, use it
            print(f"Message received: {query}")
            eel.senderText(query)

        # Main command logic
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)

            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)

                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        msg = takecommand()  # get message text
                        if msg:
                            whatsApp(Phone, msg, flag, name)
                        else:
                            speak("I didn't hear any message.")
                    elif "call" in query:
                        flag = 'call'
                        whatsApp(Phone, query, flag, name)
                    else:
                        flag = 'video call'
                        whatsApp(Phone, query, flag, name)
                else:
                    speak("Contact not found.")

            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)

            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
            
    except Exception as e:
        print(f"An error occurred in takeAllCommands: {e}")
        speak("Sorry, something went wrong.")
    
    # Always show UI and safely return something to Eel
    eel.ShowHood()
    return "done"
