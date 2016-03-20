# chardet's setup.py
from distutils.core import setup
setup(
    name = "PdfFormFiller",
    packages = ["pdfformfiller"],
    version = "0.1",
    description = "Insert text into pdf templates",
    author = "Daniel Roesler",
    author_email = "diafygi@gmail.com",
    url = "https://github.com/diafygi/pdfformfiller",
    download_url = "https://github.com/diafygi/pdfformfiller/download/0.1.tar.gz",
    keywords = ["pdf", "reportlab", "PyPDF2"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Printing",
        ],
    long_description = """\
PdfFormFiller
-------------

Source Code: https://github.com/diafygi/pdfformfiller

Documentation: https://pdfformfiller.readthedocs.org/

This is a library that lets you easy insert text into a pdf. It is super useful
when you need to prefill an existing pdf template (for example, a grant
application form) with your own data. ::

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

"""
)
