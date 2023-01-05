import tkinter as tk
import numpy as np

def change_color(j):
    global count, colors, board_lbls
    print(count)
    if count > 0:
        board_lbls[count].config(bg=colors[j])
    count += 1

root = tk.Tk()
root.geometry("540x600")

count = -6
board = np.zeros((8, 6))
board_lbls = []

# tk.frame(root)
for i in range(10):
    root.rowconfigure(i, weight=1)
for j in range(6):
    root.columnconfigure(j, weight=1)

texts = ['Peg 1', 'Peg 2', 'Peg 3', 'Peg 4', '#R', '#W']
colors = ['red', 'blue', 'green', 'black', 'white', 'yellow']

for j in range(6):
    label = tk.Label(root, text=texts[j], bg='gray', borderwidth=2, relief="groove", height=30, width=30)
    label.grid(column=j, row=0, sticky=tk.E + tk.W)

for i in range(8):
    for j in range(6):
        label = tk.Label(root, bg='gray', borderwidth=2, relief="groove", height=30)
        label.grid(column=j, row=i+1, sticky=tk.E+tk.W)
        board_lbls.append(label)

btn0 = tk.Button(root, bg=colors[0], borderwidth=2,
                relief="groove", height=30,
                command=change_color(0))
btn0.grid(column=0, row=9, sticky=tk.E+tk.W)

btn1 = tk.Button(root, bg=colors[1], borderwidth=2,
                relief="groove", height=30,
                command=change_color(1))
btn1.grid(column=1, row=9, sticky=tk.E+tk.W)

btn2 = tk.Button(root, bg=colors[2], borderwidth=2,
                relief="groove", height=30,
                command=change_color(2))
btn2.grid(column=2, row=9, sticky=tk.E+tk.W)

btn3 = tk.Button(root, bg=colors[3], borderwidth=2,
                relief="groove", height=30,
                command=change_color(3))
btn3.grid(column=3, row=9, sticky=tk.E+tk.W)

btn4 = tk.Button(root, bg=colors[4], borderwidth=2,
                relief="groove", height=30,
                command=change_color(4))
btn4.grid(column=4, row=9, sticky=tk.E+tk.W)

btn5 = tk.Button(root, bg=colors[5], borderwidth=2,
                relief="groove", height=30,
                command=change_color(5))
btn5.grid(column=5, row=9, sticky=tk.E+tk.W)

root.mainloop()