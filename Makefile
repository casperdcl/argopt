PYO = python -O

all: argopt.py
	$(PYO) $<
clean:
	rm *.py[co]
