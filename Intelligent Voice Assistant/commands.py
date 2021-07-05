from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

ERROR1 = "I did not understand! Please try again."
ERROR2 = "Item not found in todo list! Please try again."

def vocal_to_text(recognizer):
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        note = recognizer.recognize_google(audio)
        note = note.lower()
        return note

def error_message(message):
    recognizer = speech_recognition.Recognizer()
    speaker.say(message)
    speaker.runAndWait()



def create_note():
    global recognizer
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            text = vocal_to_text(recognizer)
            speaker.say("Choose a filename!")
            speaker.runAndWait()
            filename = vocal_to_text(recognizer)

            with open(f"{filename}.txt", "w") as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the notes {filename}.txt")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            error_message(ERROR1)


def add_todo():
    global recognizer
    speaker.say("What to do do you want to add?")
    speaker.runAndWait()

    done = False
    while not done:
        try:
            item = vocal_to_text(recognizer)
            todo_list.append(item)
            done = True
            speaker.say(f"I added {item} to the to do list!")
            speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            error_message(ERROR1)

def remove_todo():
    global recognizer
    speaker.say("What to do do you want to remove?")
    speaker.runAndWait()

    done = False
    while not done:
        try:
            item = vocal_to_text(recognizer)
            todo_list.remove(item)
            done = True
            speaker.say(f"I removed {item} from the to do list!")
            speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            error_message(ERROR1)

        except ValueError:
            error_message(ERROR2)

def show_todos():
    speaker.say("The items on your todo list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def greetings():
    speaker.say("Hello. What can I do for you?")
    speaker.runAndWait()

def quit():
    speaker.say("Bye!")
    speaker.runAndWait()
    sys.exit(0)
