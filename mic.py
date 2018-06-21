import speech_recognition as sr

r=sr.Recognizer() 
with sr.Microphone() as source:
    print("Please wait. Calibrating microphone...") 
    r.adjust_for_ambient_noise(source, duration=5) 
    print("Say something!")
    audio=r.listen(source)

try:
    print("Google Speech Recognition thinks you said:")
    print(r.recognize_google(audio, language="zh-TW"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("No response from Google Speech Recognition service: {0}".format(e))