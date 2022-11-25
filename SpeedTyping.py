import tkinter as tk
import time
import threading
import random
import re
import pickle
from os.path import exists


# class which allow to read the info about simulation
class Info:

    def __init__(self):
        # settings by window
        self.root = tk.Tk()
        self.root.title("Information about playing")
        self.root.geometry("300x300")
        self.root.resizable(False, False)
        self.root.config(bg='#96EEDE')

        # creating label with text which we get from loading file
        self.label = tk.Label(self.root, text=open("info.txt", "r").read(), font=("Arial", 12), bg='#BDEE96')
        self.label.pack()

        # creating button with a function of destroying the helping window
        self.button_end = tk.Button(self.root, text='Clear', font=("Arial", 16), command=self.root.destroy, bg='#BDEE96')
        self.button_end.pack()
        self.root.mainloop()


# main class - main window
class TypeSpeed:

    def __init__(self):
        # settings of the window
        self.root = tk.Tk()
        # photo = tk.PhotoImage(file='imgres.html')
        self.root.title("Typing Speed Simulation")
        self.root.wm_attributes('-alpha', 0.9)
        self.root.geometry("1200x600")
        self.root.resizable(False, False)
        self.root.config(bg='#E1C8D6')
        # self.root.iconphoto(False, photo)

        # loading number of errors from the loading file which we use for this
        if not exists("error_log.pkl"):
           pickle.dump(0, open("error_log.pkl", "wb"))
        self.error_count = pickle.load(open("error_log.pkl", "rb"))

        # loading segments of text from file
        self.texts = open("texts.txt", "r").read().split("\n")

        # creating frame
        self.frame_one = tk.Frame(self.root, bg='#B891C8')
        self.frame_one.place(relwidth=0.5, relheight=0.5)

        self.sentence = random.choice(self.texts)

        # label for text which person needs to write
        self.sample_label = tk.Label(self.frame_one, text=self.sentence, font=("Times New Roman", 16))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        # function of checking concrete symbol
        self.check = (self.root.register(self.is_valid), "%P")

        # label for writing
        self.input_entry = tk.Entry(self.frame_one, width=80, validate="key", validatecomman=self.check,
                                    font=("Helvetica", 24), background="#C5F5CC")
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)

        # label for showing speed of typing
        self.speed_label = tk.Label(self.frame_one, text="Speed: \n0 CPM\n0 WPM",
                                    font=("Times New Roman", 18))
        self.speed_label.grid(row=2, column=0, columnspan=1, padx=5, pady=10)

        # label for showing time of typing
        self.time_label = tk.Label(self.frame_one, text="Time: 0.00 sec", font=("Times New Roman", 18))
        self.time_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # label of result errors in previous attempt
        self.last_label = tk.Label(self.frame_one, text=f"Last attempt: \n{self.error_count}",
                                   font=("Times New Roman", 18))
        self.last_label.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        # label of errors in your attempt
        self.error_label = tk.Label(self.frame_one, text=f"0 errors", font=("Times New Roman", 18))
        self.error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # button of reset which can do null some pointers
        self.reset_button = tk.Button(self.frame_one, text="Reset", command=self.reset, font=("Times New Roman", 24))
        self.reset_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # button for opening info
        self.info_button = tk.Button(self.root, text="i", command=self.open_info, font=("Times New Roman", 16))
        self.info_button.place(relx=0.94, rely=0.92, relwidth=0.03, relheight=0.05)

        # hello text
        self.welcome_label = tk.Label(self.root, text="Hello, friend, you're welcome!!!", font=("Times New Roman", 24),
                                      bg='#E1C8D6')
        self.welcome_label.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.2)

        self.frame_one.place(rely=0.4, relwidth=1, relheight=0.5)

        self.error_count = 0
        self.running = False
        self.index = 0
        self.const_time = 0
        self.number_symbols = 0
        self.number_words = 0
        self.detector = True

        self.root.mainloop()

    # there we start time running
    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()

    # cpm and wpm show the actual data
    def time_thread(self):
        while self.running:
            time.sleep(0.5)
            self.const_time += 0.5
            cpm = self.number_symbols / self.const_time * 60
            wpm = self.number_words / self.const_time * 60
            self.time_label.config(text=f"Time: \n{self.const_time:.1f} sec")
            self.speed_label.config(text=f"Speed: \n{cpm:.0f} CPM\n{wpm:.0f} WPM")

    # all is clear i hope
    def reset(self):
        self.detector = True
        self.error_count = -1
        self.running = False
        self.const_time = 0
        self.number_words = 0
        self.number_symbols = 0
        self.index = 0
        self.sentence = random.choice(self.texts)
        self.speed_label.config(text="Speed: \n0 CPM\n0 WPM")
        self.time_label.config(text="Time: 0.00 sec")
        ans = pickle.load(open("error_log.pkl", "rb"))
        self.last_label.config(text=f"Last attempt: \n{ans} errors")
        self.error_label.config(text=f"0 errors")
        self.sample_label.config(text=self.sentence)
        self.input_entry.destroy
        self.input_entry = tk.Entry(self.frame_one, width=80, validate="key", validatecomman=self.check,
                                    font=("Helvetica", 24), background="#C5F5CC")
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)
        self.input_entry.after_idle(lambda: self.input_entry.configure(validate="all"))

    def open_info(self):
        Info()

    # function of checking symbol
    def is_valid(self, value):
        if (len(value) == len(self.sentence) and value[-1]
                == self.sentence[self.index]):
            self.index = 0
            self.detector = True
            self.sentence = random.choice(self.texts)
            self.speed_label.config(text="Speed: \n0 CPM\n0 WPM")
            self.sample_label.config(text=self.sentence)
            self.input_entry.after_idle(lambda: self.input_entry.configure(validate="all"))
            self.input_entry.delete(0, tk.END)
            return True
        if (len(value) != 0 and value[-1]
                == self.sentence[self.index]):
            if value[-1] == " ":
                self.number_words += 1
            self.number_symbols += 1
            self.detector = True
            self.index += 1
            self.input_entry.config(fg="#AA8DB9")
            return True
        else:
            if self.detector:
                self.error_count += 1
                self.detector = False

            self.error_label.config(text=f"{self.error_count} errors")
            pickle.dump(self.error_count, open("error_log.pkl", "wb"))
            self.input_entry.config(fg="#F0241E")
            return False


TypeSpeed()
