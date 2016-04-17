PYO = python -O

testrun: test.py
	$(PYO) $< one two
clean:
	rm -f *.py[co] argopt/*.py[co]
