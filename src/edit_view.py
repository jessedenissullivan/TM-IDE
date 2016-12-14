import Tkinter as tk
from PIL import Image, ImageTk

class Edit(tk.Frame):
	explanation = "\
Welcome to the Turing Machine editor!\n\
This is the edit screen.  \
\n\
To clear all states and transitions, enter 'clear'\n\
To add a state all states and transitions, enter 'clear'\n"

	def __init__(self, master):
		tk.Frame.__init__(self, master)

		self.draw()

	def draw(self):
		image = Image.open("./imgs/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)

		self.state_diag_label = tk.Label(self, image=self.image)	
		self.state_diag_label.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

		self.explanation_label = tk.Label(self, text=self.explanation, justify=tk.LEFT, wraplength=400)	
		self.explanation_label.grid(row=0, column=0, sticky=tk.NSEW)