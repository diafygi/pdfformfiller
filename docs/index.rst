.. pdfformfiller documentation master file, created by
   sphinx-quickstart on Sat Mar 19 21:38:58 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PdfFormFiller Documentation
===========================

.. contents::
    :depth: 1
    :local:

==========
Quickstart
==========

Source Code: https://github.com/diafygi/pdfformfiller

Welcome to the documentation for PdfFormFiller! This is a library that lets you
easy insert text into a pdf. It is super useful when you need to prefill an
existing pdf template (for example, a grant application form) with your own
data. ::

    pip install pdfformfiller

Once installed, you can add text fields to any pdf. You specify the bounding
box of the field, and the text will auto-resize to fit within that rectangle. ::

    from pdfformfiller import PdfFormFiller
    filler = PdfFormFiller("myform.pdf")
    filler.add_text(text, pagenum, (x1, y1), (x2, y2))
    filler.write(outfile)

In order to determine the correct (x1, y1), (x2, y2) coordinates for your test
field bounding box, we recommend dumping your existing pdf template to images
with 72 dpi and using an image editor (like GIMP) to find the pixel coordinates
of the rectangle you want your bounding box to be. ::

    pdftoppm -png -r 72 myform.pdf myform-pages

===========
Example use
===========

-------------
Basic Example
-------------

    Fill out a simple form by adding you name at the top of the first two
    pages.

    >>> from pdfformfiller import PdfFormFiller
    >>> filler = PdfFormFiller("myform.pdf")
    >>> filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
    >>> filler.add_text("Joe Smith", 1, (50, 50), (500, 100))
    >>> filler.write(outfile)

---------------
Default Styling
---------------

    Set some default custom styles and padding for the text fields.

    >>> from pdfformfiller import PdfFormFiller
    >>> from reportlab.lib.styles import ParagraphStyle
    >>> customstyle = ParagraphStyle("customstyle", backColor="#FF0000")
    >>> custompadding = [6, 6, 6, 6]
    >>> filler = PdfFormFiller("myform.pdf", style=customstyle, padding=custompadding)
    >>> filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
    >>> filler.add_text("Joe Smith", 1, (50, 50), (500, 100))
    >>> filler.write(outfile)

-------------
Field Styling
-------------

    Set some default custom styles and padding for one text field.

    >>> from pdfformfiller import PdfFormFiller
    >>> from reportlab.lib.styles import ParagraphStyle
    >>> customstyle = ParagraphStyle("customstyle", backColor="#FF0000")
    >>> custompadding = [6, 6, 6, 6]
    >>> filler = PdfFormFiller("myform.pdf")
    >>> filler.add_text("Joe Smith", 0, (50, 50), (500, 100), style=customstyle, padding=custompadding)
    >>> filler.add_text("Joe Smith", 1, (50, 50), (500, 100))
    >>> filler.write(outfile)

---------------
Removing Fields
---------------

    Remove the first text field on the 2nd page (will still write the
    text field on the 1st page).

    >>> from pdfformfiller import PdfFormFiller
    >>> filler = PdfFormFiller("myform.pdf", boxes=(0, 0, 255))
    >>> filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
    >>> filler.add_text("Joe Smith", 1, (50, 50), (500, 100))
    >>> del filler[1][0]
    >>> filler.write(outfile)

--------------
Bounding Boxes
--------------

    Show red bounding boxes on the page (useful for debugging).

    >>> from pdfformfiller import PdfFormFiller
    >>> filler = PdfFormFiller("myform.pdf", boxes=True)
    >>> filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
    >>> filler.add_text("Joe Smith", 1, (50, 50), (500, 100))
    >>> filler.write(outfile)

------------
Custom Boxes
------------

    Show custom blue bounding boxes on the page.

    >>> from pdfformfiller import PdfFormFiller
    >>> filler = PdfFormFiller("myform.pdf", boxes=(0, 0, 255))
    >>> filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
    >>> filler.add_text("Joe Smith", 1, (50, 50), (500, 100))
    >>> filler.write(outfile)

===
API
===

-------------
PdfFormFiller
-------------

.. autoclass:: pdfformfiller.PdfFormFiller
    :members: add_text, write

---------
TextField
---------

.. autoclass:: pdfformfiller.TextField

==============
Testing & Docs
==============

To setup a development environment, you need to clone the repo and install
dependencies. ::

    git clone https://github.com/diafygi/pdfformfiller.git
    cd pdfformfiller
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

You don't need anything extra to run the test suite. ::

    $ python test.py
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.080s

    OK

However, if you want to generate a coverage report or build the documentation,
you will need to install the developer dependencies. ::

    sudo apt-get install poppler-utils
    pip install -r dev_requirements.txt

    # to get code coverage
    coverage run --omit="venv/*" test.py
    coverage report

    # to build the docs
    cd docs
    make html

