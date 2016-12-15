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

		self.controller = master

		self.draw()

	def draw(self):
		# open and display state diagram
		image = Image.open("./imgs/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)

		self.state_diag_label = tk.Label(self, image=self.image)	
		self.state_diag_label.grid(row=0, column=1, rowspan=2, sticky='news')

		# draw explanation of screen to screen
		self.explanation_label = tk.Label(self, text=self.explanation, justify=tk.LEFT, wraplength=400)	
		self.explanation_label.grid(row=0, column=0, sticky='news')

		# draw list of transitions to screen
		self.deltas = tk.Label(self, text=self.controller.model.print_deltas(), font=("Courier", 18))
		self.deltas.grid(row=1,column=0, sticky='news')

		# draw command line for modifying model
		self.cl = tk.Entry(self)
		self.cl.grid(row=2, columnspan=2, sticky="we")

		# set window focus on command line
		self.cl.focus_set()
