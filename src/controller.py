import Tkinter as tk
from main_view import *
from model import *

class Controller(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)

		self.main = Main(self)
		self.model = Model()

		self.main.grid()