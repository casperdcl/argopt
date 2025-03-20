# IMPORTANT: for compatibility with `python -m pymake [alias]`, ensure:
# 1. Every alias is preceded by @[+]make (eg: @make alias)
# 2. A maximum of one @make alias or command per line
# see: https://github.com/tqdm/py-make/issues/1

.PHONY:
	alltests
	all
	flake8
	test
	pytest
	testsetup
	testcoverage
	testtimer
	distclean
	coverclean
	prebuildclean
	clean
	toxclean
	install_build
	install_dev
	install
	build
	buildupload
	pypi
	none

help:
	@python -m pymake -p

alltests:
	@+make testcoverage
	@+make flake8
	@+make testsetup

all:
	@+make alltests
	@+make build

flake8:
	@+pre-commit run -a flake8

test:
	tox --skip-missing-interpreters -p all

pytest:
	pytest

testsetup:
	@make help

testcoverage:
	@make coverclean
	pytest --cov=argopt --cov-report=xml --cov-report=term --cov-fail-under=80

testtimer:
	pytest

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

install:
	python -m pip install .
install_dev:
	python -m pip install -e .
install_build:
	python -m pip install -r .meta/requirements-build.txt

build:
	@make prebuildclean
	@make testsetup
	python -m build
	python -m twine check dist/*

pypi:
	python -m twine upload dist/*

buildupload:
	@make build
	@make pypi

none:
	# used for unit testing
