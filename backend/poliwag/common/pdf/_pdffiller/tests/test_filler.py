import pytest
from unittest.mock import MagicMock, patch

from ..._pdffiller import (
    PdfFormFiller
)


@pytest.fixture(scope='function')
def filler() -> PdfFormFiller:
    template = MagicMock()
    pdf_template_file = MagicMock()
    template.get_pdf_template = MagicMock(return_value=pdf_template_file)
    # Patch the pdfrw reader function
    with patch.object(PdfFormFiller, '_get_pdfrw_reader_for_template', return_value=MagicMock()):
        filler = PdfFormFiller(pdf_template=template)

    return filler


class TestPdfFillerFill:
    def test_no_error_raised_for_undefined_field(self, filler: PdfFormFiller):
        # Ensure an undefined field comes from template
        filler.pdf_template._form_reprs = ['defined_field']
        filler._get_field_value_pair_for_form_repr = lambda x: {'defined_field': 1}[x]
        filler.pdf.Root.AcroForm.Fields = [{'/T': '_undefined_field_'},]
        filler.fill()
