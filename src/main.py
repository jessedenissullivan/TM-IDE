from controller import *
import sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		app = Controller(machine=sys.argv[1], tape=sys.argv[2])
	else:
		app = Controller()
	app.mainloop()