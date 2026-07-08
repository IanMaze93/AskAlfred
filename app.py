import pyttsx3
import speech_recognition as sr
import contextlib
import os
import webbrowser
import datetime
from datetime import datetime


_tts_engine = None
_tts_error_logged = False
_mic_error_logged = False


@contextlib.contextmanager
def _suppress_stderr():
	with open(os.devnull, 'w') as devnull:
		original_stderr = os.dup(2)
		try:
			os.dup2(devnull.fileno(), 2)
			yield
		finally:
			os.dup2(original_stderr, 2)
			os.close(original_stderr)


# this method is for taking the commands and recognizing the command from the
# speech_Recognition module we will use the recongizer method for recognizing
def takeCommand():
	global _mic_error_logged

	r = sr.Recognizer()

	# from the speech_Recognition module we will use the Microphone module for listening the command
	try:
		with _suppress_stderr():
			with sr.Microphone() as source:
				print('Listening')

				# seconds of non-speaking audio before a phrase is considered complete
				r.pause_threshold = 0.7
				audio = r.listen(source, timeout=5, phrase_time_limit=10)

				try:
					print("Recognizing")

					#setting for english
					Query = r.recognize_google(audio, language='en-in')
					print("the command is printed=", Query)

				except sr.UnknownValueError:
					print("No speech recognized. Falling back to typed command.")
					return input("Type your command: ")
				except Exception as e:
					print(e)
					print("Say that again sir")
					return input("Type your command: ")

				return Query
	except sr.WaitTimeoutError:
		print("No speech detected. Falling back to typed command.")
		return input("Type your command: ")
	except Exception as e:
		if not _mic_error_logged:
			print(f"Microphone unavailable, falling back to typed commands: {e}")
			_mic_error_logged = True
		return input("Type your command: ")

def _get_tts_engine():
	global _tts_engine
	global _tts_error_logged

	if _tts_engine is not None:
		return _tts_engine

	try:
		engine = pyttsx3.init()
		voices = engine.getProperty('voices')
		if voices:
			engine.setProperty('voice', voices[0].id)
		_tts_engine = engine
		return _tts_engine
	except Exception as e:
		if not _tts_error_logged:
			print(f"TTS unavailable, falling back to text output: {e}")
			_tts_error_logged = True
		return None


def speak(audio):
	engine = _get_tts_engine()
	if engine is None:
		print(f"Alfred: {audio}")
		return

	# Method for the speaking of the assistant
	engine.say(audio)

	# Blocks while processing all the currently queued commands
	engine.runAndWait()

def tellDay():
	# get current datetime
	dt = datetime.now()
	#Speak the day of the week
	speak("The day is " + dt.strftime('%A'))


def tellTime():
	time = datetime.now()
	#convert time into speakable string
	print(time)
	currentTime = str(time.today().strftime("%I:%M %p"))
	speak("Master Wayne, the time is " + currentTime)

def Hello():
	
	#triggers greeting
	speak("Hello Master Wayne. how may I help you")


def Take_query():

	#triggers a greeting from Alfred
	Hello()
	
	#Continue to loop until command to shutdown
	while(True):
		try:
			query = takeCommand()
		except KeyboardInterrupt:
			speak("Goodbye Master Wayne")
			break

		if not query or query == "None":
			continue

		#Lower Case Queries work the best
		query = query.lower()

		if "tell me your name" in query:
			speak("I am Alfred. Your Virtual Assistant")

		elif "alfred i have a question" in query:
			speak("What is your question sir")
			#ask alfred your question
			query = takeCommand().lower()
			speak("Displaying the results on the bat computer Master Wayne")
			#displays the search results from your default internet browser
			webbrowser.open(f"{str(query)}")
			continue

		elif "alfred play pandora" in query:
			speak("Playing music Master Wayne")
			webbrowser.open("www.pandora.com")
			
		elif "alfred what's today" in query:
			tellDay()
			continue
		
		elif "alfred what time is it" in query:
			tellTime()
			continue
		
		# this will exit and terminate the program
		elif "alfred shut down" in query:
			speak("Goodbye Master Wayne")
			exit()

if __name__ == '__main__':
	# main method 
	Take_query()
