from pprint import PrettyPrinter
import pdb
from graphviz import Digraph

pprint = PrettyPrinter()

# Draw nodes in graphviz graph
def add_nodes(graph, nodes):
	print('add_nodes')
	for n in nodes:
		#print n
		if isinstance(n, tuple):
			graph.node(*n[0], **n[1])
		else:
			graph.node(*n)
	return graph

# Draw edges in graphviz graph
def add_edges(graph, edges):
	print('add_edges')
	for e in edges:
		if isinstance(e[0], tuple):
			graph.edge(*e[0], **e[1])
		else:
			graph.edge(*e)
	return graph

# Model TM for TM-SIM
# binds following:
#
class Model(object):
	# Classes used during computation
	comp_hist = 'Computational History:'

	def __init__(self, controller, machine=None, tape=None):
		self.controller = controller

		# State variables of 7-tuple
		self.states = {'0'}			# 0 is always the start state
		self.accept = set()
		self.reject = set()
		self.start = 0
		self.head = 0 		# this turing machine does not have an infinite number of blanks on either side, they are added dynamically 
		self.initial_tape = []
		self.tape = []
		self.delta = {}
		self.sigma = {}
		self.gamma = {}

		self.init_TM(machine, tape)

	# if machine saved, parse machine into simulator
	def parse_machine(self, machine):
		with open(machine,'r') as f:
			delta_source = f.readlines()

		label = ''
		hold_over = False
		for line in delta_source:  # read machine source line by line
			if '{' in line:				# beginning of graph encoding, skip
				continue
			elif line == '}':			# end of graph encoding, break from loop
				break
			elif '->' in line:			# line is edge, add states to states, transitions to delta, and all char to sigma and gamma
				state_trans = [x.strip() for x in line.split('[')[0].strip().split('->')]			# get state transition
				if 'label' in line:		# labeled edge, parse label for transition
					label = line.split('label=')[1].split(']')[0].decode('utf-8')  # read in label, decode b/c of arrow char \u2192

					self.states |= set(state_trans)				# add states, duplicates ignored b/c using python set

					trans = label.strip('"').split(u'\u2192')	# strip label of double quotes and split on right arrow
					readchar = trans[0]							# first char to left is char read on transition

					if ',' in trans[1]:
						writechar = trans[1].split(',')[0]		# trans reads, writes, and shifts
						shift = trans[1].split(',')[1]
					else:										# trans only reads and shifts
						writechar = None
						shift = trans[1]

					if shift == u'R':							# Convert shift to numerical value
						shift = 1
					elif shift == u'L':
						shift = -1
					else:
						shift = 0
				else:											# unlabeled transition, set non-state vals to null
					readchar = None
					writechar = None
					shift = 0

				# Add new rule to delta transitions
				self.delta[ state_trans[0], readchar ] = state_trans[1], writechar, shift
			else:														#  Line is node
				self.states |= {line.split('[')[0].strip()}				#  Add state to collection of states
				label = line.split('label=')[1].split()[0]
				
				if 'start' in label:									#  label is marked as start state, add trans from 0 to here
					print("Found start state")
					self.delta[0,None] = line.split('[')[0].strip(), None, 0
				if 'accept' in label:									#  Node is accept state, add to set of accept states
					self.accept |= {line.split('[')[0].strip()}
				if 'reject' in label:									#  Node is reject state, add to set of reject states
					self.reject |= {line.split('[')[0].strip()}

	# set up TM simulator
	def init_TM(self,machine=None, tape=None):
		if machine:				# load saved TM if there is one
			self.parse_machine(machine)

		if tape:				# load tape if one specified
			with open(tape, 'r') as f:
				self.initial_tape = f.readline()
		else:					# else initialize everything to null sets
			self.delta = {}
			self.states = set([0])
			self.accept = set([])
			self.reject = set([])
			self.initial_tape = '_'		# null val for tape is a single blank char

		self.tape = self.initial_tape  # init tape to modifiable buffer

		#pprint.pprint(self.delta)
		if ('0', None) in self.delta:
			# set currstate to init state of TM (what 0 points to and first char of tape)
			self.currstate = self.delta['0', None][0], self.tape[self.head]  

		self.print_state_diagram()

	# manually add new delta transition to TM
	# called from edit screen
	def add_delta(self, userInput):
		valid = True
		state1 = state2 = read = write = shift = None

		pre_img = userInput.split('-')[0]
		img = userInput.split('-')[1]

		pre_img = pre_img.split(',')
		img = img.split(',')

		if len(pre_img)==2:
			state1 = pre_img[0]
			read = pre_img[1]
		elif len(pre_img)==1:
			state = pre_img[0]
		else:
			valid = False

		if len(img)==3:
			state2 = img[0]
			write = img[1]
			shift = img[2]
		elif len(img)==2:
			state2 = img[0]
			shift = img[1]
		elif len(img)==1:
			state2 = img[0]
		else:
			valid = False

		if shift.lower() == 'l':
			shift = -1
		elif shift.lower() == 'r':
			shift = 1
		else:
			shift = 0

		if valid:
			self.delta[state1, read] = state2, write, shift

	# clear TM (not tape)
	def clear(self):
		# State variables of 7-tuple
		self.states = {'0'}			# 0 is always the start state
		self.accept = set()
		self.reject = set()
		self.start = 0
		self.head = 0 		# this turing machine does not have an infinite number of blanks on either side, they are added dynamically 
		self.tape = []
		self.delta = {}
		self.sigma = {}
		self.gamma = {}	

	# reintialize TM with original tape, state, and head pos
	def reset_tm(self, event=None):
		print("reset tm")
		self.tape = self.initial_tape
		self.head = 0
		self.currstate = self.delta['0',None][0], self.tape[self.head]
		self.comp_hist = 'Computational History:'

	# Advance TM one step, mapped to enter in main
	# returns print out of configuration after step
	def step_TM(self):
		print("step tm")
		pprint.pprint("previous tm: " + self.tape)
		# current state is an accept or reject state, reset TM
		if self.currstate[0] in self.accept or self.currstate[0] in self.reject:
			self.controller.reset_model(event=None)

		# get transition
		try:
			self.nextstep = self.delta[self.currstate]
		except:
			self.comp_hist += "\nThe turing machine crashed\n\
cannot transition from %s on %s.\n\
Restarting the turing machine." % (self.currstate[0], self.currstate[1])
			self.reset_model()
			pprint.pprint("Reset tm: " + self.tape)
			return self.get_config()

		# write char to tape if writing
		if self.nextstep[1]:
			self.tape = self.tape[:self.head] + self.nextstep[1] + self.tape[self.head+1:]

		# head over edge of right end of tape, add blank char to right of tape
		if self.head == (len(self.tape)-1):
			#pdb.set_trace()
			self.tape += '_'
		
		# head over edge of left end of tape, add blank char to left of tape and inc head by 1
		elif self.head == 0:
			self.head += 1
			self.tape = '_' + self.tape

		# shift head if shifting
		self.head += self.nextstep[2]

		# set new current state
		try:
			self.currstate = self.nextstep[0], self.tape[self.head]
		except:
			pdb.set_trace()

		# print new state diagram
		self.print_state_diagram()

		# if sim now in accept state, inform user
		if self.currstate[0] in self.accept or self.currstate[0] in self.reject:
			pprint.pprint("Halted tm: " + self.tape)
			return "\nThe turing machine is finished\nPressing enter will restart the turing machine."
		
		# return next line of comp history
		else:
			pprint.pprint("Stepped tm: " + self.tape)
			return self.get_config()

	# Create current config and save to comp history
	def get_config(self):
		print("get config tm")
		#  There is no tape or defined current state, return empty
		if not self.tape or 'currstate' not in dir(self):
			return

		# set string val inside [] of single config line in comp history
		if self.currstate[0] in self.accept:
			state_name = 'q_accept'
		elif self.currstate[0] in self.reject:
			state_name = 'q_reject'
		else:
			state_name = 'q_%s' % (self.currstate[0])

		t = '\n%s[%s]%s' % (''.join(self.tape[:self.head]), state_name, ''.join(self.tape[self.head:]))

		# return new configure
		return t


	# print state diagram of current configuration
	# draw state diagram to the screens folder with title temp
	def print_state_diagram(self):
		print('model_print_state_diagram')
		dot = Digraph()
		states = []
		transitions = []

		for s in self.states:
			if s in self.accept:
				label = (str(s), {'label':"q_accept"})
			elif s in self.reject:
				label = (str(s), {'label':"q_reject"})
			else:
				label = (str(s), {'label':str(s)})

			if s == self.currstate[0]:
				label[1]['color'] = 'red'
				label[1]['weight'] = '5'

			states += [label]

		for preimage, image in self.delta.iteritems():
			if preimage[1]:
				label = u'%s \u2192 ' % (max(preimage[1], ''))
				
				if image[1]:
					label += u'%s,' % (max(image[1],''))

				if image[2]>0:
					label += u'R'
				elif image[2]==0:
					label += u'S'
				elif image[2]<0:
					label += u'L'
				
				key = str(preimage[0]), str(image[0])
				transitions += [ ( (key), {'label':label } ) ]

		dot.format = 'gif'
		add_edges(add_nodes(dot, states), transitions).render('imgs/temp')

	# return list of delta transitions
	def print_deltas(self):
		delta_str = ""
		ordered_dict = sorted([x for x in self.delta.keys()])
		for x in ordered_dict:
			preimg = x
			img = self.delta[x]
			delta_str += u"%s,%s \u2192 " % (preimg[0], max(' ',preimg[1]))
			delta_str += u"%s,%s," % (img[0], max(' ',img[1]))
			if img[2] > 0:
				delta_str += "R\n"
			elif img[2] < 0:
				delta_str += "L\n"
			else:
				delta_str += "S\n"

		return delta_str