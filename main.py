import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np

# Initialize chat history
chatStr = ""

# Function for AI-based conversation
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    
    # Generate AI response using OpenAI's language model
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Speak the response
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    # Generate AI response for the given prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Store the response in a file
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)


def say(text):
    # Speak the provided text using the OS system command
    os.system(f'say "{text}"')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Listen to user's speech using the microphone
        audio = r.listen(source)
        try:
            print("Recognizing...")
            # Convert speech to text using Google's speech recognition service
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    
    while True:
        print("Listening...")
        query = takeCommand()
        
        # Check for specific commands
        
        # Open websites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        
        # Play music
        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")
        
        # Get the current time
        elif "the time" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {min} minutes")
        
        # Open FaceTime app
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")
        
        # Open Passky app
        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")
        
        # Generate AI response for a prompt
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        
        # Quit Jarvis
        elif "Jarvis Quit".lower() in query.lower():
            exit()
        
        # Reset chat history
        elif "reset chat".lower() in query.lower():
            chatStr = ""
        
        else:
            print("Chatting...")
            # Have a conversation with the AI
            chat(query)

        # say(query)