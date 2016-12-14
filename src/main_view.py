import Tkinter as tk
from PIL import Image, ImageTk

class Main(tk.Frame):
	explanation = "\tWelcome to the Turing Machine editor!\n\
This is the main screen.\n\
Press enter to step through the turing machine.  \
The current state is highlighted in red while the computational history (configurations) are \
on the left.\n\
\n\
To edit the turing machine, press e\n\
To quit the program, press q\n\
to reset the turing machine, press r"

	def __init__(self, master):
		tk.Frame.__init__(self, master)

		self.draw()

	def draw(self):
		image = Image.open("../imgs/temp.gif")
		self.image = ImageTk.PhotoImage(image)

		self.state_diag_label = tk.Label(self, image=self.image)	
		self.state_diag_label.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

		self.explanation_label = tk.Label(self, text=self.explanation, justify=tk.LEFT, wraplength=400)	
		self.explanation_label.grid(row=0, column=0, sticky=tk.NSEW)