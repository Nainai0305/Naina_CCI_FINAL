import speech_recognition as sr
from pythonosc.udp_client import SimpleUDPClient
import time

negative_words_filtered = [
    "unfair", "biased", "racist", "sexist", "discriminates", "prejudiced", "prejudice", "unjust", "racism",
    "oppression", "oppressed", "freedom", "inequality", "crime", "defeat", "weak", "war", "hate", "slave", "slavery",
    "intolerance", "wrong", "suicide", "death", "kill", "abortion", "discrimination", "injustice", "immoral", "corruption",
    "violence", "terror", "xenophobia", "homophobia", "transphobia", "misogyny", "sexism", "harassment", "bullying", "abuse",
    "poverty", "censorship", "surveillance", "authoritarian", "protest", "activism", "resistance", "rebellious", "radical",
    "extremist", "not fair", "not right", "not acceptable", "no", "not true", "bad", "disagree", "mean", "lie", "died",
    "cheat", "dishonest", "fraud", "scam", "die", "control", "problem", "issue", "hate", "dislike", "weird", "strange",
    "wrong", "negative", "doubt", "uncertain", "skeptical", "critical", "criticize", "fault", "flaw", "error",
    "misunderstanding", "fake", "conspiracy", "don't care", "don't want", "detest", "despise", "scorn", "contempt",
    "anger", "rage", "frustration", "annoyance", "unhappy", "unrest", "think", "thoughts", "opinion", "belief","my view", "truth", "true", "think",
    "notion", "idea", "concept", "viewpoint", "perspective", "standpoint", "position", "stance", "fight", "struggle", "race", "discrimnate", "discrimination", "unfair",
    "not fair", "not right", "excluded", "deny", "unfairly", "I exist", "I deserve", "I am real", "I am human", "I have rights", "I matter",
    "I am important", "I am valid", "I am worthy", "I am enough", "I am loved", "I am accepted", "I am supported", "I am valued", "freedom", "liberty", "human rights", "autonomy", 
    "self-determination", "dignity", "respect", "equality", "justice", "skin color", "race", "different", "diversity", "unique", "inidividual", "identity", "skin color", "negatively", 
    "negative", "vocabulary", "vocab", "bad", "racism", "do not", "don't", "view"
]

# This script listens for speech input and sends OSC messages to TouchDesigner when it detects any of the negative words from the list.

# OSC client to send to TouchDesigner
osc_client = SimpleUDPClient("127.0.0.1", 8000)

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said:", text)

            # Check for negative word
            for phrase in negative_words_filtered:
                if phrase in text.lower():
                    osc_client.send_message("/negative", 1)
                    time.sleep(0.5)
                    osc_client.send_message("/negative", 0)
                    

        except Exception as e:
            print("Error:", e)
