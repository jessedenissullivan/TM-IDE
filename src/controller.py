import Tkinter as tk
from os import system
from main_view import *
from edit_view import *
from model import *

class Controller(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)

		self.main = Main(self)
		self.edit = Edit(self)
		self.model = Model()

		system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

		self.main.grid(row=0, column=0, sticky='news')
		self.edit.grid(row=0, column=0, sticky='news')

		self.bind('<Return>', self.show_frame)

	def show_frame(self, page_name):
		vars(self)['main'].tkraise()
