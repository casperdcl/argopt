PYO = python -O

testrun: argopt.py
	$(PYO) $< one two
clean:
	rm *.py[co]
