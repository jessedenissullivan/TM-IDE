import pdb
import Tkinter as tk
from os import system
from main_view import *
from edit_view import *
from model import *

class Controller(tk.Tk):
	def __init__(self, *args, **kwargs):
		# init window object
		tk.Tk.__init__(self)

		# init model, all command line args passed to init of model (machine and tape)
		self.model = Model(controller = self, *args, **kwargs)

		# Key bindings for each window { <window name> : { <key> : <function> } }
		self.bindings = {
			'Main':{
				'<Return>':self.step_model,
				'q':self.quit,
				'r':self.reset_model,
				'e':lambda event: self.show_frame('Edit'),
				'd':lambda event: pdb.set_trace()
			},	
			'Edit':{
				'<Return>':self.process_cl,
				'q':lambda event: self.show_frame('Main'),
				'c':self.clear,
				'e':lambda event: self.show_frame('Edit'),
				'd':lambda event: pdb.set_trace()
			}
		}

		# build all views in main window
		self.frames = {}
		for F in (Main, Edit):
			self.frames[F.__name__] = F(self)
			self.frames[F.__name__].grid(row=0, column=0, sticky='news')

		# switch display focus to controller window (OS X only)
		system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

		# set main view and key bindings to main
		self.show_frame('Main')

	# process command line on edit view
	def process_cl(self, event):
		pass

	# quit program
	def quit(self, event):
		self.destroy()

	# switch view to requested view
	# switch key bindings to appropriate view
	def show_frame(self, page_name):
		# raise view
		self.frames[page_name].tkraise()

		# set key bindings
		for k,v in self.bindings[page_name].iteritems():
			self.bind(k,v)

	# clear model
	# update comp history on main view
	# update state diagram on main view
	def clear(self, event):
		self.model.clear()
		self.reset_model(event)

	# step model
	# update comp history on main view
	# update state diagram on main view
	def step_model(self, event):
		print("step model")
		new_config = self.model.step_TM()
		self.frames['Main'].update(new_config=new_config, new_state_diag="./imgs/temp.gif")

	# set model back to initial state (machine and tape)
	# update comp history on main view
	# update state diagram on main view
	def reset_model(self, event):
		print("reset model")
		# reset model
		self.model.reset_tm()
		
		# reset comp history
		self.frames['Main'].comp_hist.delete(0, tk.END)
		self.frames['Main'].comp_hist.insert(tk.END, "Computation History:")
		
		# reset state diagram
		#self.model.print_state_diagram()
		self.frames['Main'].update(new_state_diag="./imgs/temp.gif")