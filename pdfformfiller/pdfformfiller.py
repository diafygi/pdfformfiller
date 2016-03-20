from io import BytesIO
from collections import namedtuple, defaultdict
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet
try:
    basestring
except NameError:
    basestring = str

TextField = namedtuple("TextField",
    ["text", "x1", "y1", "width", "height", "style", "padding"])
"""
This is a namedtuple class used for storing text field parameters in a
:class:`.PdfFormFiller` instance. Note: Coordinates in this class are based on the origin
(0, 0) as the bottom left.

Attributes:
    text (str): Contents of the text field
    x1 (int or float): X-coord for bottom left bounding box corner
    y1 (int or float): Y-coord for bottom left bounding box corner
    width (int or float): Width of bounding box
    height (int or float): Height of bounding box
    style (ParagraphStyle or None): Optional custom style of text field
    padding (tuple or None): Optional custom padding for text field
"""

DEFAULT_STYLE = getSampleStyleSheet()['Normal']
DEFAULT_STYLE.fontName="times"
DEFAULT_STYLE.fontSize = 20
DEFAULT_STYLE.leading = 24
DEFAULT_PADDING = (0, 0, 0, 0)
DEFAULT_BOX_COLOR = (255, 0, 0)

class PdfFormFiller(defaultdict):
    """Add text fields to a PDF. Useful for programmatically filling out forms.

    Args:
        pdf (str or file): The pdf to which to add text fields. Can be a string
            path to a file, or a file-like object.

    Keyword Args:
        style (ParagraphStyle): Custom style to apply to text fields. Default
            is black text, 20pt Times New Roman.
        padding (tuple): Custom padding to apply to the text field. Tuple
            is a series of four floats or integers (leftPadding,
            bottomPadding, rightPadding, topPadding). Default is
            ``[0, 0, 0, 0]``.
        boxes (bool or tuple): Whether to show the text field bounding boxes in
            the final pdf. Can be ``False`` (default), ``True`` (default color
            red), or an ``(r, g, b)`` tuple for the bounding box color.

    Attributes:
        N (list[:class:`.TextField`]): List of the added text fields for page N.
            For example, to delete the 2nd text field from the 4th page, do
            ``del filler[3][1]``. Note: This attribute is an integer, not "N".

    Note:
        Coordinates use ``points``, which represent 1/72 inch. The origin for
        ``(0, 0)`` is at the top left of the page. This is slightly different
        than normal pdf coordinates (which have the origin at the bottom left).
        We use a top left origin because it is easier to figure out bounding box
        coordinates using image editing software (which typically use a top left
        origin). You can quickly dump the pdf to a set of images at the correct
        dpi using ``pdftoppm``::

            pdftoppm -png -r 72 myform.pdf myform

    """
    def __init__(self, pdf, style=DEFAULT_STYLE, padding=DEFAULT_PADDING, boxes=False):
        super(PdfFormFiller, self).__init__(lambda: [])
        self.pdf = PdfFileReader(open(pdf, "rb") if isinstance(pdf, basestring) else pdf)
        self.style = style
        self.padding = padding
        self.boxes = DEFAULT_BOX_COLOR if boxes and not isinstance(boxes, (list, tuple)) else boxes

    def add_text(self, text, pagenum, upperLeft, lowerRight, style=None, padding=None):
        """Add a text field with a bounding box.

        Insert some text within a certain rectangle on a page. Text will be
        resized if needed to fit within the rectangle. NOTE: coordinates are
        measured from the top left of the page (i.e. top left is (0, 0)).

        Args:
            text (str): Contents of the text field
            pagenum (int): Page of the pdf to insert the field (0 is first page)
            upperLeft (tuple): (x, y) coordinates for top left corner
                of bounding box rectangle
            lowerRight (tuple): (x, y) coordinates for bottom right corner
                of bounding box rectangle

        Keyword Args:
            style (ParagraphStyle): Custom style to apply to the text. Default
                is None (i.e. inherit style from class default).
            padding (tuple): Custom padding to apply to the text field. Tuple
                is a series of four floats or integers (leftPadding,
                bottomPadding, rightPadding, topPadding). Default is None (i.e.
                inherit padding from class default).

        Returns:
            None
        """

        # input origin is top left, needs to switch to bottom left
        mediaBox = self.pdf.getPage(pagenum).mediaBox
        x1 = upperLeft[0]
        x2 = lowerRight[0]
        y1 = mediaBox[3] - mediaBox[1] - lowerRight[1]
        y2 = mediaBox[3] - mediaBox[1] - upperLeft[1]

        self[pagenum].append(TextField(
            text=text,
            x1=x1,
            y1=y1,
            width=(x2 - x1),
            height=(y2 - y1),
            style=style,
            padding=(padding or self.padding),
        ))

    def write(self, outputFile):
        """Writes the modified pdf to a file.

        This method merges the original pdf with all of the added text fields
        together to create the final modified pdf. Text fields are written over
        top of the original pdf.

        Args:
            outputFile (str or file): Output file to write to. Can be string
                path or any file-like object.

        Returns:
            None
        """

        # iterate through original pdf pages
        output = PdfFileWriter()
        for pagenum in xrange(self.pdf.numPages):
            existing_page = self.pdf.getPage(pagenum)

            # insert text fields if any for this page
            if len(self[pagenum]) > 0:
                mediaBox = self.pdf.getPage(pagenum).mediaBox
                pagesize = (mediaBox[2] - mediaBox[0], mediaBox[3] - mediaBox[1])
                packet = BytesIO()
                canvas = Canvas(packet, pagesize=pagesize)
                if self.boxes:
                    canvas.setStrokeColorRGB(*self.boxes)

                for field in self[pagenum]:
                    frame = Frame(field.x1, field.y1, field.width, field.height,
                        *field.padding, showBoundary=bool(self.boxes))
                    style = field.style or self.style
                    story = [Paragraph(field.text, style)]
                    story_inframe = KeepInFrame(field.width, field.height, story)
                    frame.addFromList([story_inframe], canvas)

                canvas.save()
                packet.seek(0)
                new_pdf = PdfFileReader(packet)
                existing_page.mergePage(new_pdf.getPage(0))
            output.addPage(existing_page)

        # write the final pdf to the file
        if isinstance(outputFile, basestring):
            outputFile = open(outputFile, "wb")
            output.write(outputFile)
            outputFile.close()
        else:
            output.write(outputFile)

