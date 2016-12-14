import Tkinter as tk
from PIL import Image, ImageTk

class Main(tk.Frame):
	explanation = "Welcome to the Turing Machine editor!\n\n\
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

		self.controller = master

		self.draw()

	def draw(self):
		image = Image.open("./imgs/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)

		self.state_diag_label = tk.Label(self, image=self.image)	
		self.state_diag_label.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

		self.explanation_label = tk.Label(self, text=self.explanation, justify=tk.LEFT, wraplength=400)	
		self.explanation_label.grid(row=0, column=0, sticky='nw')

		# draw computational history to comp_history label on screen
		self.comp_hist = tk.Listbox(self)

		# init comp history and draw
		self.comp_hist.insert(tk.END, "Computation History:")
		self.comp_hist.grid(row=1, column=0, sticky='news')

	# update all new values
	def update(self, new_config=None, new_state_diag=None):
		if new_config:
			self.comp_hist.insert(tk.END, new_config)
		if new_state_diag:
			# update state diagram
			image = Image.open('./imgs/temp.gif')
			self.image = ImageTk.PhotoImage(image)
			self.state_diag_label.configure(image = self.image)