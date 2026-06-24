import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import json
import os
import winsound

# ----------------------------
# TEXT TO SPEECH
# ----------------------------
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ----------------------------
# BACKGROUND MUSIC
# ----------------------------
def play_music():
    try:
        winsound.PlaySound("background.wav",
                           winsound.SND_ASYNC | winsound.SND_LOOP)
    except:
        print("Music file not found")

# ----------------------------
# SAVE FILE
# ----------------------------
SAVE_FILE = "game_state.json"

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"room": "start", "level": 0}

def save_game(state):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(state, f)
    except:
        print("Save error")

# ----------------------------
# RIDDLES
# ----------------------------
riddles = [

("I speak without a mouth and hear without ears. I have no body but come alive with wind. (Hint: sound reflection)", "echo"),

("I have keys but no locks. I have space but no room. You can enter but cannot go outside. (Hint: computer device)", "keyboard"),

("What has hands but cannot clap? (Hint: tells time)", "clock"),

("The more you take, the more you leave behind. What am I? (Hint: walking)", "footsteps"),

("I’m tall when I’m young and short when I’m old. What am I? (Hint: melts)", "candle")

]

# ----------------------------
# ESCAPE ROOM CLASS
# ----------------------------
class EscapeRoom:

    def __init__(self, root):

        self.root = root
        self.root.title("Escape Room Game")
        self.root.geometry("650x550")

        self.state = load_game()

        # IMAGE DISPLAY
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # TEXT DISPLAY
        self.text_label = tk.Label(root, text="", wraplength=600, font=("Arial", 12))
        self.text_label.pack(pady=10)

        # PROGRESS LABEL
        self.progress_label = tk.Label(root, text="", font=("Arial", 10))
        self.progress_label.pack()

        # INPUT BOX
        self.entry = tk.Entry(root, width=30)
        self.entry.pack()

        # SUBMIT BUTTON
        self.button = tk.Button(root, text="Submit Answer", command=self.process_command)
        self.button.pack(pady=10)

        # RESTART BUTTON
        restart_button = tk.Button(root, text="Restart Game", command=self.restart_game)
        restart_button.pack(pady=5)

        self.update_room()

    # ----------------------------
    # RESTART GAME
    # ----------------------------
    def restart_game(self):

        self.state = {"room": "start", "level": 0}
        save_game(self.state)
        self.update_room()

    # ----------------------------
    # SHOW IMAGE
    # ----------------------------
    def show_image(self, file):

        try:
            img = Image.open(file)
            img = img.resize((450,300))
            img = ImageTk.PhotoImage(img)

            self.image_label.config(image=img)
            self.image_label.image = img

        except:
            print("Image not found:", file)

    # ----------------------------
    # UPDATE ROOM
    # ----------------------------
    def update_room(self):

        room = self.state["room"]

        if room == "start":

            self.show_image("start_room.png")

            text = """
You wake up trapped in a mysterious room.

A message on the wall says:

"Solve all 5 riddles to escape."

Type: start
"""

            self.text_label.config(text=text)
            self.progress_label.config(text="")
            speak("Solve all riddles to escape.")

        elif room == "riddle":

            self.show_image("puzzle_room.png")

            level = self.state["level"]
            question = riddles[level][0]

            self.progress_label.config(text=f"Progress: Riddle {level+1} / 5")

            self.text_label.config(text=question)

            speak("Solve the riddle.")

        elif room == "escaped":

            self.show_image("escape.png")

            self.text_label.config(text="You solved all riddles. The door opens. You escaped!")
            self.progress_label.config(text="Completed!")

            messagebox.showinfo("Victory","You escaped the room!")
            speak("Congratulations you escaped!")

            # RESET GAME
            self.state = {"room": "start", "level": 0}
            save_game(self.state)

    # ----------------------------
    # PROCESS COMMAND
    # ----------------------------
    def process_command(self):

        command = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)

        room = self.state["room"]

        if room == "start":

            if command == "start":
                self.state["room"] = "riddle"

        elif room == "riddle":

            level = self.state["level"]
            answer = riddles[level][1]

            if command == answer:

                speak("Correct answer")

                self.state["level"] += 1

                if self.state["level"] == 5:
                    self.state["room"] = "escaped"

            else:
                speak("Wrong answer. Try again.")

        save_game(self.state)
        self.update_room()

# ----------------------------
# MAIN PROGRAM
# ----------------------------
if __name__ == "__main__":

    play_music()

    root = tk.Tk()
    game = EscapeRoom(root)
    root.mainloop()