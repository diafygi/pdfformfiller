import unittest
from io import BytesIO
from hashlib import sha256
from base64 import b64decode
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from reportlab.lib.styles import ParagraphStyle

from src.pdfformfiller import PdfFormFiller

class TestPdfFormFiller(unittest.TestCase):
    """ Tests for PdfFormFiller """

    def setUp(self):
        "Reset the original pdf file's pointer"
        self.pdf = BytesIO(hello_world_pdf)
        self.out = BytesIO()

    def assertHashOutput(self, pdf, known_hash):
        "Compare png image of pdf to known sha256 hash"
        # Uncomment to save pdf to disk (used for looking at results)
        # pdf.seek(0); out = open("out.pdf", "wb"); out.write(pdf.read()); out.close();
        pdf.seek(0)
        p = Popen(["pdftoppm", "-png", "-r", "72", "-f", "1", "-l", "1", "-"],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(input=pdf.read())
        if err:
            raise IOError(err)
        pdf_hash = sha256(out).hexdigest()
        self.assertEqual(pdf_hash, known_hash,
            "pdf hash ({}) doesn't match expected hashes ({})".format(
                pdf_hash, known_hash))

    def test_no_fields(self):
        "Still exports even when no text fields are added"
        filler = PdfFormFiller(self.pdf)
        filler.write(self.out)
        self.assertHashOutput(self.out, "726d27c0809a73cedde958cb204a897c8f81fc367ca2aadc8101e6d38be8a9c5")

    def test_string_output_path(self):
        "can write to string outputFile"
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        tmpout = NamedTemporaryFile()
        filler.write(tmpout.name)
        self.assertHashOutput(tmpout, "d961e57867788345a3bc0ea3adaa34bb81bc439848f30472302bad6ce8e1b3a6")

    def test_add_fields(self):
        "Can add several text fields"
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.add_text("Joe Smith", 0, (50, 200), (500, 250))
        filler.write(self.out)
        self.assertHashOutput(self.out, "e2813583628380bc084cdede1531739034f2823849bcb9339368abe845af00d7")

    def test_inlude_boxes(self):
        "Red field boxes appear debugging"
        filler = PdfFormFiller(self.pdf, boxes=True)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "bf1bcef99f6de11bdf542f40eebd47f1dfc4861e5ec4d6ce65d0acd9228abd2e")

    def test_custom_boxes(self):
        "Blue field boxes appear debugging"
        filler = PdfFormFiller(self.pdf, boxes=(0, 0, 255))
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "2dd58978209ddd2c531987d5b12115ea7729e87e7aa7115b09cc18aa5ff45fef")

    def test_custom_default_style(self):
        "custom default small text style"
        customstyle = ParagraphStyle("customstyle", fontSize=8)
        filler = PdfFormFiller(self.pdf, style=customstyle)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "c60753864a1cb130519856f0a1bb0ab51ab0fcbea7baa4f36f5e101bfe6409b0")

    def test_custom_field_style(self):
        "custom default small text style"
        customstyle = ParagraphStyle("customstyle", fontSize=8)
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100), style=customstyle)
        filler.write(self.out)
        self.assertHashOutput(self.out, "c60753864a1cb130519856f0a1bb0ab51ab0fcbea7baa4f36f5e101bfe6409b0")

    def test_custom_default_padding(self):
        "custom default small text style"
        custompadding = [6, 6, 6, 6]
        filler = PdfFormFiller(self.pdf, padding=custompadding)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "2a195aa2ce8a1cc40465cffb39bcc187bd4555679611589083b8019fbe0933ef")

    def test_custom_field_padding(self):
        "custom default small text style"
        custompadding = [6, 6, 6, 6]
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100), padding=custompadding)
        filler.write(self.out)
        self.assertHashOutput(self.out, "2a195aa2ce8a1cc40465cffb39bcc187bd4555679611589083b8019fbe0933ef")


# Hello World example pdf
hello_world_pdf = b64decode("""\
JVBERi0xLjQNCiWTjIueIFJlcG9ydExhYiBHZW5lcmF0ZWQgUERGIGRvY3VtZW50IGh0dHA6Ly93
d3cucmVwb3J0bGFiLmNvbQ0KMSAwIG9iag0KPDwgL0YxIDIgMCBSIC9GMiAzIDAgUiA+Pg0KZW5k
b2JqDQoyIDAgb2JqDQo8PCAvQmFzZUZvbnQgL0hlbHZldGljYSAvRW5jb2RpbmcgL1dpbkFuc2lF
bmNvZGluZyAvTmFtZSAvRjEgL1N1YnR5cGUgL1R5cGUxIC9UeXBlIC9Gb250ID4+DQplbmRvYmoN
CjMgMCBvYmoNCjw8IC9CYXNlRm9udCAvVGltZXMtUm9tYW4gL0VuY29kaW5nIC9XaW5BbnNpRW5j
b2RpbmcgL05hbWUgL0YyIC9TdWJ0eXBlIC9UeXBlMSAvVHlwZSAvRm9udCA+Pg0KZW5kb2JqDQo0
IDAgb2JqDQo8PCAvQ29udGVudHMgOCAwIFIgL01lZGlhQm94IFsgMCAwIDYxMiA3OTIgXSAvUGFy
ZW50IDcgMCBSIC9SZXNvdXJjZXMgPDwgL0ZvbnQgMSAwIFIgL1Byb2NTZXQgWyAvUERGIC9UZXh0
IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJIF0gPj4gL1JvdGF0ZSAwIC9UcmFucyA8PCAgPj4gDQog
IC9UeXBlIC9QYWdlID4+DQplbmRvYmoNCjUgMCBvYmoNCjw8IC9PdXRsaW5lcyA5IDAgUiAvUGFn
ZU1vZGUgL1VzZU5vbmUgL1BhZ2VzIDcgMCBSIC9UeXBlIC9DYXRhbG9nID4+DQplbmRvYmoNCjYg
MCBvYmoNCjw8IC9BdXRob3IgKGFub255bW91cykgL0NyZWF0aW9uRGF0ZSAoRDoyMDE2MDMxOTE4
MDEzNSswOCcwMCcpIC9DcmVhdG9yIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSB3d3cucmVwb3J0
bGFiLmNvbSkgL0tleXdvcmRzICgpIC9Nb2REYXRlIChEOjIwMTYwMzE5MTgwMTM1KzA4JzAwJykg
L1Byb2R1Y2VyIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSB3d3cucmVwb3J0bGFiLmNvbSkgDQog
IC9TdWJqZWN0ICh1bnNwZWNpZmllZCkgL1RpdGxlICgpIC9UcmFwcGVkIC9GYWxzZSA+Pg0KZW5k
b2JqDQo3IDAgb2JqDQo8PCAvQ291bnQgMSAvS2lkcyBbIDQgMCBSIF0gL1R5cGUgL1BhZ2VzID4+
DQplbmRvYmoNCjggMCBvYmoNCjw8IC9GaWx0ZXIgWyAvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNv
ZGUgXSAvTGVuZ3RoIDE3OSA+Pg0Kc3RyZWFtDQpHYXBRaDBFPUYsMFVcSDNUXHBOWVReUUtrP3Rj
PklQLDtXI1UxXjIzaWhQRU1fVFBzI2I3dSQqPDBZOEMiXWYtLz90XU9AQGcjXz1XKTFkX0FINFY7
YTtyMmYyQW1kKEtpOUtpPSZEIzdqVFcoIz8kQEdlXWBhO3QuWSpxIUJPSUtAIy9oW3EkNXN0YjNC
P21CaVY+byYuQExTZT1VSDxVQCIhU1tVcWsuVyEhQ18xNzB+PmVuZHN0cmVhbQ0KZW5kb2JqDQo5
IDAgb2JqDQo8PCAvQ291bnQgMCAvVHlwZSAvT3V0bGluZXMgPj4NCmVuZG9iag0KeHJlZg0KMCAx
MA0KMDAwMDAwMDAwMCA2NTUzNSBmDQowMDAwMDAwMDc1IDAwMDAwIG4NCjAwMDAwMDAxMTkgMDAw
MDAgbg0KMDAwMDAwMDIyOSAwMDAwMCBuDQowMDAwMDAwMzQxIDAwMDAwIG4NCjAwMDAwMDA1Mzgg
MDAwMDAgbg0KMDAwMDAwMDYyNSAwMDAwMCBuDQowMDAwMDAwOTE3IDAwMDAwIG4NCjAwMDAwMDA5
NzkgMDAwMDAgbg0KMDAwMDAwMTI1MyAwMDAwMCBuDQp0cmFpbGVyDQo8PCAvSUQgDQogJSBSZXBv
cnRMYWIgZ2VuZXJhdGVkIFBERiBkb2N1bWVudCAtLSBkaWdlc3QgKGh0dHA6Ly93d3cucmVwb3J0
bGFiLmNvbSkNCiBbKFwzMDJcKVwzNjVcMjI3XDAzM1wyMTVUXDI2M1wzNTNdXDMzNjFcMzI2XDAx
MjJOKSAoXDMwMlwpXDM2NVwyMjdcMDMzXDIxNVRcMjYzXDM1M11cMzM2MVwzMjZcMDEyMk4pXQ0K
IC9JbmZvIDYgMCBSIC9Sb290IDUgMCBSIC9TaXplIDEwID4+DQpzdGFydHhyZWYNCjEzMDINCiUl
RU9GDQo=""")

if __name__ == '__main__':
    unittest.main()

