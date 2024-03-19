import speech_recognition as S#converting voice to speech
import pyttsx3 as P#converting text to speech
import urllib#for opening the url's
import pyautogui as pg#for doing interacting with the system
import pywhatkit as pw#for opening youtube and other websites
import keyboard as kb#for clicking keyboard keys
import datetime as dt#for getting the date and time
import pyjokes#for access the jokes
from time import sleep#for giving a delay between actions
import os#for interacting with os
from playsound import playsound#used to play sound

recogniser=S.Recognizer()#accessing the recogniser from speech_recognition module

engine=P.init()#initialising the enigne from pyttsx3 module 
voice=engine.getProperty('voices')
engine.setProperty('voice',voice[0].id)#voice[0] for male and voice[1] for female
engine.setProperty('rate',130)#adjusting the speed of the voice

def speak(command):
    engine.say(command)#converts the command into speech
    engine.runAndWait()#wait for some time after speaking

def connected():#check if you are connected to internet or not
    try:
        urllib.request.urlopen('https://www.google.com',timeout=2)
        return True
    except urllib.error.URLError as error:
        return False
    except:
        return False

#function that converts speech to text
def voice_command_processor():
    with S.Microphone() as source:#accessing the primary microphone as the source
        recogniser.adjust_for_ambient_noise(source,duration=0.2)
        playsound("sounds/open.wav")
        audio = recogniser.listen(source,phrase_time_limit=3)#listening continuously to the speech for 4 seconds
        text = ''#creating empty string to store the text converted form speech
        try:
            print("recognizing....")
            text=recogniser.recognize_google(audio)#using google speech recognition
            text=text.lower()#converting the text to lowercase
        except S.UnknownValueError as e:
            print(e)#printing the error if occured any
        except S.RequestError as e:
            speak("service is down.")
            print("service is down")
            return("service is down")
        playsound("sounds/close.wav")
        return text.lower()
    
#function to search for something
def search(command):
    string=""
    if "search for" in command:#looking for "search for" key in the given command        
        string=command.split("search for")#exactly splitting the command at "search for" key
        """
            command : could you please search for bommalu
            output : ['could you please','bommalu']
            string[1] : bommalu  --- accessing the 2nd element from the list
        """
        speak(f'Searching {string[1]}')
        pw.search(string[1])
    elif "search" in command:
        #same like above, instead "search" is used
        string=command.split("search")
        speak(f"Searching {string[1]}")
        pw.search(string[1])

class time_date():
    time=dt.datetime.now().strftime("%I %M %p")#to get time --- %I : hrs, %M : minutes, %p : seconds
    time_24=dt.datetime.now().strftime("%H")#to get hours in 24h format
    date=dt.datetime.now().strftime("%d %B %Y")#to get date --- %d : Date, %B : Month, %Y : Year
    day=dt.datetime.now().strftime("%A")#to get day
    today = dt.date.today()
    y_date = today-dt.timedelta(days=1)#subtracting 1 day from current date to get yesterday's date
    t_date = today+dt.timedelta(days=1)#adding 1 day to current date to get tomorrow's date
    dy_date = today-dt.timedelta(days=2)#subtracting 2 days from current date to get day before yesterday's date
    dt_date = today+dt.timedelta(days=2)#adding 2 days from current date to get day after tomorrow's date
obj=time_date()

def play(command):
    song=command.split("play")#exactly splitting the command at "play" key
    """
        command : could you please play bavalu song
        output : ['could you please','bavalu song']
        song[1] : bavalu song  --- accessing the 2nd element from the list
    """
    if song!="":
        print("playing "+song[1])
        speak("playing"+song[1])
        pw.playonyt(song[1])#open youtube and search for the song
        kb.press("space")#press enter to play the song

def open(command):
    command = command.split("open")#exactly splitting the command at "open" key
    """
        command : could you please open chrome
        output : ['could you please','chrome']
        command[1] : chrome  --- accessing the 2nd element from the list
    """
    speak(f'opening {command[1]}')
    pg.press("win")#press the win key
    sleep(0.5)
    kb.write(command[1])#enter the command
    sleep(0.5)
    kb.press("enter")#click enter

def y_t_date(command):
    if "today's" in command or "today" in command:
        print(obj.date)
        speak("today's date is "+str(obj.date))
    elif "day after tomorrow" in command or "day after tomorrow's" in command:
        print(obj.dt_date)
        speak("day after tomoerrow's date is "+str(obj.dt_date))
    elif "day before yesterday" in command or "day before yesterday's" in command:
        print(obj.dy_date)
        speak("day before yesterday's date is "+str(obj.dy_date))
    elif "yesterday's" in command or "yesterday" in command:
        print(obj.y_date)
        speak("yesterday's date is "+str(obj.y_date))
    elif "tomorrow's" in command or "tomorrow" in command:
        print(obj.t_date)
        speak("tomorrow's date is "+str(obj.t_date))
    elif "date" in command:
        print(obj.date)
        speak("today's date is "+str(obj.date))

def executable(command):
    num=[2,1]
    if "your name" in command or "who are you" in command:
        speak("My name is Elite, i'm your voice assistant")
        print("My name is The Elite, i'm your voice assistent")
    elif command=="":
        pass
    elif "time" in command:
        print(obj.time)
        speak("the time is "+str(obj.time))
    elif "date" in command:
        y_t_date(command)
    elif "joke" in command and "tell" in command:
        joke=pyjokes.get_joke()
        print(joke)
        speak(joke)
    elif "open" in command:
        open(command)
    elif "play" in command:
        play(command)
    elif "search" in command:
        search(command)
    elif "bye" in command or "good bye" in command:
        speak("Bye")
    elif "shutdown" in command:
        speak("The system will Shutdown in, 3")
        playsound("sounds/beep.wav")
        for i in num:
            speak(i)
            playsound("sounds/beep.wav")
            if i==1:
                print(True)
                #os.system("shutdown /s /t 5")
    elif "restart" in command or "restart the system" in command:
        speak("The system will restart in, 3")
        playsound("sounds/beep.wav")
        for i in num:
            speak(i)
            playsound("sounds/beep.wav")
            if i==1:
                print(True)
                #os.system("shutdown /r /t 5")
    elif "logout" in command or "logout from the system" in command:
        speak("Logging out")
        os.system("shutdown /l /t 0")