FLAKE8_FLAGS = --show-source
MYPY_FLAGS = --pretty
YAPF_FLAGS =
ISORT_FLAGS =

PY_PROJ = phyeng

all: fmt ck

ck: flake8 mypy

flake8: ${PY_PROJ}/*.py
	flake8 ${FLAKE8_FLAGS} $^

mypy: ${PY_PROJ}/*.py
	mypy ${MYPY_FLAGS} $^

fmt: yapf isort

yapf: ${PY_PROJ}/*.py
	yapf -i ${YAPF_FLAGS} $^

isort: ${PY_PROJ}/*.py
	isort ${ISORT_FLAGS} $^
