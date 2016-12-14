import pdb
import Tkinter as tk
from os import system
from main_view import *
from edit_view import *
from model import *

class Controller(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self)

		self.model = Model(*args, **kwargs)

		self.frames = {}
		for F in (Main, Edit):
			self.frames[F.__name__] = F(self)
			self.frames[F.__name__].grid(row=0, column=0, sticky='news')

		system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

		self.bind('<Return>', self.step_model)

		self.show_frame('Main')

	# switch view to requested view
	def show_frame(self, page_name):
		self.frames[page_name].tkraise()

	# step model, update comp history on main view
	def step_model(self, event):
		new_config = self.model.step_TM()
		self.frames['Main'].update(new_config=new_config, new_state_diag="./imgs/temp.gif")