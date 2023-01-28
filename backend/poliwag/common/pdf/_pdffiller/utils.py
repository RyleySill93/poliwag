import io
from typing import Dict, Optional, Tuple, Type
import logging
# @TODO Get rid of this dependency
from django.utils.text import slugify
import pdfrw
from pdfrw.pdfreader import PdfReader

from .templates import PdfFormTemplate
from . import fields


logger = logging.getLogger(__name__)

ANNOT_FIELD_KEY = '/T'          # Label for form field
ANNOT_FORM_TYPE = '/FT'         # Form type (e.g. text/button)
ANNOT_FORM_BUTTON = '/Btn'      # Type for buttons selectors on/off
ANNOT_FORM_TEXT = '/Tx'         # Type for straight textbox
ANNOT_FORM_CHECK = '/Ch'        # Type for combobox/checkbox (even dropdown select)


def get_clean_field_repr_from_pdfrw_field(field: pdfrw.PdfDict) -> str:
    return field[ANNOT_FIELD_KEY][1:-1]


def get_field_type(field: pdfrw.PdfDict) -> str:
    field_types = {
        ANNOT_FORM_BUTTON: 'BUTTON',
        ANNOT_FORM_TEXT: 'TEXT',
        ANNOT_FORM_CHECK: 'CHECKBOX',
    }

    try:
        field_type = field_types[field[ANNOT_FORM_TYPE]]
    except KeyError:
        field_type = f'Unknown field type: {field[ANNOT_FORM_TYPE]}'

    # if field_type == 'CHECKBOX':
    #     # @TODO field['Opt'] may have available options for multi select
    #     # See country combo box example in tests

    return field_type


class FormFieldConverter:
    """
    Attempts to go from pdfrw field to pdf filler field
    """
    TOGGLE_VALUES = {
        pdfrw.PdfName('Yes'),
        pdfrw.PdfName('No'),
        pdfrw.PdfName('On'),
        pdfrw.PdfName('Off'),
    }

    def convert(self, field) -> fields.AbstractPdfFormField:
        field_type = get_field_type(field)
        meta = {}
        if field_type == 'CHECKBOX':
            if isinstance(field.Opt, pdfrw.PdfArray):
                meta['choices'] = []
                for choices in field.Opt:
                    choice = choices[0][1:-1]
                    meta['choices'].append(choice)

            pdf_filler_field_cls = fields.SelectFormField

        elif field_type == 'BUTTON':
            if field.Kids:
                meta['choices'] = []
                for kid in field.Kids:
                    keys = kid.AP.N.keys()
                    choices = [key[1:] for key in keys if key not in self.TOGGLE_VALUES]
                    meta['choices'].extend(choices)

                pdf_filler_field_cls = fields.RadioFormField

            else:
                pdf_filler_field_cls = fields.ToggleFormField

        else:
            pdf_filler_field_cls = fields.TextFormField

        return pdf_filler_field_cls(form_repr=field[ANNOT_FIELD_KEY][1:-1], **meta)

class PdfFormUtils:
    def __init__(self, file_path: str=None, pdf_template: Optional[PdfFormTemplate]=None, pdfrw_reader: Optional[PdfReader]=None):
        if file_path:
            self.pdf = pdfrw.PdfReader(file_path)
        elif pdf_template:
            self.pdf = pdfrw.PdfReader(pdf_template.get_pdf_template())
        elif pdfrw_reader:
            self.pdf = pdfrw_reader
        else:
            raise ValueError('Missing `file_path` or `pdf_template` args')

    def convert(self):
        """
        Attempts to match pdfrw fields to PdfForm fields and attached meta
        data where applicable types.
        """
        converter = FormFieldConverter()
        print('\nConversion\n--------------------------')
        for form_repr, field in self.get_fields_by_form_reprs().items():
            pdf_filler_field = converter.convert(field)
            print(pdf_filler_field)
        print('\n--------------------------')

    def describe(self):
        """
        Use this function to quickly explore available
        form fields
        """
        print('\n\nDescription\n====================================')
        self.describe_file()
        self.describe_form_fields()
        self.convert()
        print('\n====================================')

    def describe_file(self):
        info = self._get_pdf_info()
        if not info:
            print('No Info Available')
            return

        title = info.Title
        creator = info.Creator
        producer = info.Producer
        created_at = info.CreationDate
        modified_at = info.ModDate

        print('\nFile Details\n--------------------------')
        print(f'\ttitle       : {title}')
        print(f'\tcreator     : {creator}')
        print(f'\tproducer    : {producer}')
        print(f'\tcreated_at  : {created_at}')
        print(f'\tmodified_at : {modified_at}')
        print('\n--------------------------')

    def describe_form_fields(self):
        fields = self.get_fields_by_form_reprs()
        print('\nForm Fields\n--------------------------')
        for form_repr, field in fields.items():
            field_type = get_field_type(field)
            print(f'\t{form_repr}: {field_type}')
        print('\n--------------------------')

    def _get_pdf_info(self):
        return self.pdf.Info

    def get_converted_field_by_form_repr(self, form_repr) -> fields.AbstractPdfFormField:
        fields_by_form_reprs = self.get_fields_by_form_reprs()
        converter = FormFieldConverter()
        field = fields_by_form_reprs[form_repr]
        return converter.convert(field)

    def get_fields_by_form_reprs(self) -> Dict[str, pdfrw.PdfDict]:
        """
        Use this function to quickly explore available
        form fields
        """
        return {
            get_clean_field_repr_from_pdfrw_field(field): field
            for field in self.pdf.Root.AcroForm.Fields
        }

    def normalize_form_fields(self):
        """
        Use this to help building a form
        # @TODO Should this be part of the final version?
        """
        for field in self.pdf.Root.AcroForm.Fields:
            if field.T:
                normalized_type = slugify(field.T)
                normalized_type = normalized_type.replace('-', '_')
                field.T = pdfrw.PdfString(f'({normalized_type})')

    def write(self, file_name: str):
        """
        Writes pdf file to disk
        """
        pdfrw.PdfWriter().write(file_name, self.pdf)
        logger.debug(f'Wrote new pdf: {file_name}')

    def write_to_buffer(self, file_buffer: io.BytesIO=None, file_name: Optional[str]=None) -> io.BytesIO:
        """
        Return a buffer containing the pdf
        """
        if not file_buffer:
            # Name the buffer if an existing one isn't provided
            file_buffer = io.BytesIO()
            file_buffer.name = file_name

        pdfrw.PdfWriter().write(file_buffer, self.pdf)
        file_buffer.seek(0)
        return file_buffer
