# PdfFormFiller

[![Build Status](https://travis-ci.org/diafygi/pdfformfiller.svg?branch=master)](https://travis-ci.org/diafygi/pdfformfiller)
[![Coverage Status](https://coveralls.io/repos/github/diafygi/pdfformfiller/badge.svg?branch=master&badge=1)](https://coveralls.io/github/diafygi/pdfformfiller?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pdfformfiller/badge/?version=latest)](http://pdfformfiller.readthedocs.org/en/latest/?badge=latest)

This is a python library that lets you easily insert text into a pdf. It is
super useful when you need to prefill an existing pdf template (for example, a
grant application form) with your own data.

```
pip install pdfformfiller
```

## Documentation

https://pdfformfiller.readthedocs.org/

## Basic Example

```py
from pdfformfiller import PdfFormFiller
filler = PdfFormFiller("myform.pdf")
filler.add_text(text, pagenum, (x1, y1), (x2, y2))
filler.write(outfile)
```

## Development

To setup a development environment, you need to clone the repo and install
dependencies.

```sh
git clone https://github.com/diafygi/pdfformfiller.git
cd pdfformfiller
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# run tests
python test.py
```

If you want to generate a coverage report or build the documentation, you will
need to install the developer dependencies.

```sh
sudo apt-get install poppler-utils
pip install -r dev_requirements.txt

# to get code coverage
coverage run --omit="venv/*" test.py
coverage report

# to build the docs
cd docs
make html
```

