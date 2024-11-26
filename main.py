import pandas as pd
import random
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
FONT="Ariel"
FLIP_TIME=3000
current_card={}
flip_timer=None
to_learn={}

def word_known():
    to_learn.remove(current_card)
    to_learn_data=pd.DataFrame(to_learn)
    to_learn_data.to_csv('./data/words_to_learn.csv',index=False)
    next_card()

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card=random.choice(to_learn)
        french_word=current_card["French"]
        card_canvas.itemconfig(card_image,image=card_front_img)
        card_canvas.itemconfig(card_title, text="French",fill="black")
        card_canvas.itemconfig(card_word, text=french_word,fill="black")
        flip_timer = window.after(FLIP_TIME, flip_card)
    except:
        card_canvas.itemconfig(card_image,image=card_front_img)
        card_canvas.itemconfig(card_title, text="No more unknown words.",fill="black")
        card_canvas.itemconfig(card_word, text="Finished.",fill="black")


def flip_card():
    card_canvas.itemconfig(card_title, text="English",fill="white")
    card_canvas.itemconfig(card_word, text=current_card["English"],fill="white")
    card_canvas.itemconfig(card_image,image=card_back_img)

try:
    csv_data=pd.read_csv("./data/words_to_learn.csv")
except:
    original_data=pd.read_csv("./data/french_words.csv")
    to_learn=original_data.to_dict(orient="records")
else:
    to_learn=csv_data.to_dict(orient="records")
current_card=random.choice(to_learn)

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer=window.after(FLIP_TIME, func=flip_card)

# images
card_front_img=PhotoImage(file="./images/card_front.png")
card_back_img=PhotoImage(file="./images/card_back.png")
right_img=PhotoImage(file="./images/right.png")
wrong_img=PhotoImage(file="./images/wrong.png")

#canvas
card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image=card_canvas.create_image(400, 263, image=card_front_img)
card_title=card_canvas.create_text(400, 150, text="French", fill="black", font=(FONT, 40, "italic"))
card_word=card_canvas.create_text(400, 263, text=current_card["French"], fill="black", font=(FONT, 60, "bold"))
card_canvas.grid(row=0, column=0,columnspan=2)

#Buttons
unknown_button=Button(image=wrong_img,highlightthickness=0,command=next_card)
unknown_button.grid(row=1, column=0)

known_button=Button(image=right_img,highlightthickness=0,command=word_known)
known_button.grid(row=1, column=1)


window.mainloop()
