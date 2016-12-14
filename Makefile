all:	src/main.py
	python src/main.py machine_and_tape/machine.txt machine_and_tape/tape.txt

clean:
	-rm src/*.pyc