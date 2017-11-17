# IMPORTANT: for compatibility with `python setup.py make [alias]`, ensure:
# 1. Every alias is preceded by @[+]make (eg: @make alias)
# 2. A maximum of one @make alias or command per line
#
# Sample makefile compatible with `python setup.py make`:
#```
#all:
#	@make test
#	@make install
#test:
#	nosetest
#install:
#	python setup.py install
#```

.PHONY:
	alltests
	all
	flake8
	test
	testnose
	testsetup
	testcoverage
	testtimer
	distclean
	coverclean
	prebuildclean
	clean
	installdev
	install
	build
	pypimeta
	pypi
	none

alltests:
	@+make testcoverage
	@+make flake8
	@+make testsetup

all:
	@+make alltests
	@+make build

flake8:
	@+flake8 --max-line-length=80 --count --statistics --exit-zero argopt/
	@+flake8 --max-line-length=80 --count --statistics --exit-zero examples/
	@+flake8 --max-line-length=80 --count --statistics --exit-zero .
	@+flake8 --max-line-length=80 --count --statistics --exit-zero argopt/tests/

test:
	tox --skip-missing-interpreters

testnose:
	nosetests argopt -d -v

testsetup:
	python setup.py check --restructuredtext --strict
	python setup.py make none

testcoverage:
	@make coverclean
	nosetests argopt --with-coverage --cover-package=argopt --cover-erase --cover-min-percentage=80 -d -v

testtimer:
	nosetests argopt --with-timer -d -v

distclean:
	@+make coverclean
	@+make prebuildclean
	@+make clean
prebuildclean:
	@+python -c "import shutil; shutil.rmtree('build', True)"
	@+python -c "import shutil; shutil.rmtree('dist', True)"
	@+python -c "import shutil; shutil.rmtree('argopt.egg-info', True)"
coverclean:
	@+python -c "import os; os.remove('.coverage') if os.path.exists('.coverage') else None"
	@+python -c "import shutil; shutil.rmtree('argopt/__pycache__', True)"
	@+python -c "import shutil; shutil.rmtree('argopt/tests/__pycache__', True)"
clean:
	@+python -c "import os; import glob; [os.remove(i) for i in glob.glob('*.py[co]')]"
	@+python -c "import os; import glob; [os.remove(i) for i in glob.glob('argopt/*.py[co]')]"
	@+python -c "import os; import glob; [os.remove(i) for i in glob.glob('examples/*.py[co]')]"
	@+python -c "import os; import glob; [os.remove(i) for i in glob.glob('argopt/tests/*.py[co]')]"

installdev:
	python setup.py develop --uninstall
	python setup.py develop

install:
	python setup.py install

build:
	@make prebuildclean
	python setup.py sdist --formats=gztar,zip bdist_wheel
	python setup.py bdist_wininst

pypimeta:
	python setup.py register

pypi:
	twine upload dist/*

buildupload:
	@make testsetup
	@make build
	@make pypimeta
	@make pypi

none:
	# used for unit testing
