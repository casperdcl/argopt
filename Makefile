PYO = python -O

all: argopt.py
	$(PYO) $< one two
clean:
	rm *.py[co]
