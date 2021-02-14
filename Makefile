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
	toxclean
	installdev
	install
	build
	buildupload
	pypi
	none

help:
	@python setup.py make -p

alltests:
	@+make testcoverage
	@+make flake8
	@+make testsetup

all:
	@+make alltests
	@+make build

flake8:
	@+flake8 -j 8 --count --statistics --exit-zero .

test:
	tox --skip-missing-interpreters -p all

testnose:
	nosetests -d -v tests/

testsetup:
	python setup.py check --metadata --restructuredtext --strict
	python setup.py make none

testcoverage:
	@make coverclean
	nosetests --with-coverage --cover-package=argopt --cover-erase --cover-min-percentage=80 -d -v tests/

testtimer:
	nosetests --with-timer -d -v tests/

distclean:
	@+make coverclean
	@+make prebuildclean
	@+make clean
prebuildclean:
	@+python -c "import shutil; shutil.rmtree('build', True)"
	@+python -c "import shutil; shutil.rmtree('dist', True)"
	@+python -c "import shutil; shutil.rmtree('argopt.egg-info', True)"
	@+python -c "import shutil; shutil.rmtree('.eggs', True)"
	@+python -c "import os; os.remove('argopt/_dist_ver.py') if os.path.exists('argopt/_dist_ver.py') else None"
coverclean:
	@+python -c "import os; os.remove('.coverage') if os.path.exists('.coverage') else None"
	@+python -c "import os, glob; [os.remove(i) for i in glob.glob('.coverage.*')]"
	@+python -c "import shutil; shutil.rmtree('argopt/__pycache__', True)"
	@+python -c "import shutil; shutil.rmtree('tests/__pycache__', True)"
clean:
	@+python -c "import os, glob; [os.remove(i) for i in glob.glob('*.py[co]')]"
	@+python -c "import os, glob; [os.remove(i) for i in glob.glob('argopt/*.py[co]')]"
	@+python -c "import os, glob; [os.remove(i) for i in glob.glob('examples/*.py[co]')]"
	@+python -c "import os, glob; [os.remove(i) for i in glob.glob('tests/*.py[co]')]"
toxclean:
	@+python -c "import shutil; shutil.rmtree('.tox', True)"


installdev:
	python setup.py develop --uninstall
	python setup.py develop

install:
	python setup.py install

build:
	@make prebuildclean
	@make testsetup
	python setup.py sdist bdist_wheel
	# python setup.py bdist_wininst

pypi:
	twine upload dist/*

buildupload:
	@make build
	@make pypi

none:
	# used for unit testing
