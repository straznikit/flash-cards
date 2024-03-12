from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/german.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="German", fill="black")
    canvas.itemconfig(card_word, text=current_card["German"], fill="black")
    canvas.itemconfig(card_background, image=front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"],  fill="white")
    #canvas.itemconfig -> pierwsza rzecz w nawiasie to rzecz którą chcemy skonfigurować,
    # po przecinku piszemy co chcemy w niej zmienić)
    canvas.itemconfig(card_background, image=card_back_image)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

#3000=3sec
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file='images/card_front.png')
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
button2 = Button(image=right_image, highlightthickness=0, command=is_known)
button2.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
button1 = Button(image=wrong_image, highlightthickness=0, command=next_card)
button1.grid(column=0, row=1)

next_card()

window.mainloop()