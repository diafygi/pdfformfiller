import unittest
from hashlib import sha256
from StringIO import StringIO
from base64 import b64decode
from tempfile import NamedTemporaryFile
from reportlab.lib.styles import ParagraphStyle

from src.pdfformfiller import PdfFormFiller

class TestPdfFormFiller(unittest.TestCase):
    """ Tests for PdfFormFiller """

    def setUp(self):
        "Reset the original pdf file's pointer"
        self.pdf = StringIO(hello_world_pdf)
        self.out = StringIO()

    def assertHashOutput(self, pdf, known_hash):
        "Compare pdf sha256 hash to known hash"
        # Uncomment to save pdf to disk (used for looking at results)
        # pdf.seek(0); out = open("out.pdf", "wb"); out.write(pdf.read()); out.close();
        pdf.seek(0)
        pdf_hash = sha256(pdf.read()).hexdigest()
        self.assertEqual(pdf_hash, known_hash,
            "pdf hash ({}) doesn't match expected hash ({})".format(
                pdf_hash, known_hash))

    def test_no_fields(self):
        "Still exports even when no text fields are added"
        filler = PdfFormFiller(self.pdf)
        filler.write(self.out)
        self.assertHashOutput(self.out, "f6526f729e0ef207ef10425fbe7fd87bf4fc3c03e61f026a88f2addc3a9a3179")

    def test_string_output_path(self):
        "can write to string outputFile"
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        tmpout = NamedTemporaryFile()
        filler.write(tmpout.name)
        self.assertHashOutput(tmpout, "07925c2d87ec34f46457d0bc2f4edee02d9f197520ef502d0f4a2057350e3121")

    def test_add_fields(self):
        "Can add several text fields"
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.add_text("Joe Smith", 0, (50, 200), (500, 250))
        filler.write(self.out)
        self.assertHashOutput(self.out, "95999787b497949a3e99edc01c7bb25502a59baba76d3de5da127993ba5ac492")

    def test_inlude_boxes(self):
        "Red field boxes appear debugging"
        filler = PdfFormFiller(self.pdf, boxes=True)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "d1ce470e34a1026292eac7645995addd232ab332964732f1981ca51a270a0093")

    def test_custom_boxes(self):
        "Blue field boxes appear debugging"
        filler = PdfFormFiller(self.pdf, boxes=(0, 0, 255))
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "c5fa450428828ada91e9b7966b0d23d00d48a9af4a4f33fb1aa84d64ba9d1ca5")

    def test_custom_default_style(self):
        "custom default small text style"
        customstyle = ParagraphStyle("customstyle", fontSize=8)
        filler = PdfFormFiller(self.pdf, style=customstyle)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "8678b49b76b4703277ff07e76fba3e6f4032c62a812fec86b056c2ace7cb3f64")

    def test_custom_field_style(self):
        "custom default small text style"
        customstyle = ParagraphStyle("customstyle", fontSize=8)
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100), style=customstyle)
        filler.write(self.out)
        self.assertHashOutput(self.out, "8678b49b76b4703277ff07e76fba3e6f4032c62a812fec86b056c2ace7cb3f64")

    def test_custom_default_padding(self):
        "custom default small text style"
        custompadding = [6, 6, 6, 6]
        filler = PdfFormFiller(self.pdf, padding=custompadding)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100))
        filler.write(self.out)
        self.assertHashOutput(self.out, "915c3437dba9f6670839346665bcb6d75a9b760e46f520be26cdcb248fa4236d")

    def test_custom_field_padding(self):
        "custom default small text style"
        custompadding = [6, 6, 6, 6]
        filler = PdfFormFiller(self.pdf)
        filler.add_text("Joe Smith", 0, (50, 50), (500, 100), padding=custompadding)
        filler.write(self.out)
        self.assertHashOutput(self.out, "915c3437dba9f6670839346665bcb6d75a9b760e46f520be26cdcb248fa4236d")


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

