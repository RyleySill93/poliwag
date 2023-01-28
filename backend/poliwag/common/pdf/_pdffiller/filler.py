import io
import logging
from typing import Optional, Tuple
import pdfrw

from .templates import PdfFormTemplate
from .fields import AbstractPdfFormField
from .utils import PdfFormUtils


logger = logging.getLogger(__name__)


class PdfFormFiller:
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    def __init__(self, pdf_template: PdfFormTemplate):
        self.pdf_template = pdf_template.prepare()
        self.pdf = self._get_pdfrw_reader_for_template(pdf_template)
        if self.pdf.Root.AcroForm:
            self.pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        else:
            logger.debug(f'{pdf_template} is not a form')

        self.utility = PdfFormUtils(pdfrw_reader=self.pdf)

    @property
    def _fields(self) -> list:
        # Support rendering pdfs that lack forms
        if self.pdf.Root.AcroForm is None:
            logger.debug(f'no fields detected to fill')
            return []

        return self.pdf.Root.AcroForm.Fields

    def _get_pdfrw_reader_for_template(self, pdf_template: PdfFormTemplate):
        template_file = pdf_template.get_pdf_template()
        return pdfrw.PdfReader(template_file)

    def fill(self):
        # Acrobat form / pdfescape.com fields included here
        for pdfrw_field in self._fields:
            form_repr = pdfrw_field[self.ANNOT_FIELD_KEY][1:-1]
            # Check if form_repr is defined inside template
            if form_repr not in self.pdf_template._form_reprs:
                # Not defined
                continue

            field, value = self._get_field_value_pair_for_form_repr(form_repr)
            if field and value is not None:
                field.fill(pdfrw_field, value)
            else:
                logger.debug(f'unrecognized form repr: {form_repr}')

    def _get_field_value_pair_for_form_repr(self, form_repr: str) -> Tuple[AbstractPdfFormField, any]:
        return self.pdf_template.get_field_value_pair_for_form_repr(form_repr)

    def write(self, file_name: Optional[str]=None):
        """
        Writes pdf file to disk
        """
        file_name = file_name or self.pdf_template.get_pdf_file_name()
        return self.utility.write(file_name=file_name)

    def write_to_buffer(self, file_buffer: io.BytesIO=None, file_name: Optional[str]=None) -> io.BytesIO:
        """
        Return a buffer containing the pdf
        """
        file_name = file_name or self.pdf_template.get_pdf_file_name()
        return self.utility.write_to_buffer(file_buffer=file_buffer, file_name=file_name)
