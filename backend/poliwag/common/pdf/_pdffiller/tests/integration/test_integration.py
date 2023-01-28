from .conftest import PDF_FORM_EXAMPLE_FP
from ...._pdffiller import (
    PdfFormTemplate,
    PdfFormFiller,
    fields,
)

# @TODO Add support for PdfFormTotal and form_function_field

class PdfFormExample(PdfFormTemplate):
    first_name = fields.TextFormField(form_repr='given_name_text_box', required=True)
    last_name = fields.TextFormField(form_repr='family_name_text_box')
    address_1 = fields.TextFormField()
    house_number = fields.TextFormField()
    address_2 = fields.TextFormField()
    postcode = fields.TextFormField()
    city = fields.TextFormField()
    radio = fields.RadioFormField(choices=['choice1', 'choice2', 'choice3'])
    country = fields.SelectFormField(form_repr='country_combo_box', choices=['Austria', 'Belgium', 'Croatia'])
    gender = fields.SelectFormField(form_repr='gender_box', choices=['Man', 'Woman'])
    height_cm = fields.TextFormField(form_repr='height_formatted_field')
    has_driver_license = fields.ToggleFormField(form_repr='driver_license_check_box')
    speaks_deutsch = fields.ToggleFormField(form_repr='language_1_check')
    speaks_english = fields.ToggleFormField(form_repr='language_2_check')
    speaks_french = fields.ToggleFormField(form_repr='language_3_check')
    speaks_esperanto = fields.ToggleFormField(form_repr='language_4_check')
    speaks_latin = fields.ToggleFormField(form_repr='language_5_check')
    favorite_color = fields.SelectFormField(form_repr='favorite_color_list_box', choices=['Red', 'Blue', 'Green', 'Yellow'])

    def get_pdf_template(self):
        return PDF_FORM_EXAMPLE_FP

def test_describe_pdf_form():
    template = PdfFormExample(first_name='John')
    filler = PdfFormFiller(pdf_template=template)
    filler.utility.describe()

def test_pdf_full_fill():
    template = PdfFormExample(
        first_name='John',
        last_name='Doe',
        address_1='Fake Address',
        house_number=123,
        postcode=12345,
        city='Somewhere',
        radio='choice3',
        country='Croatia',
        gender='Woman',
        height_cm=180,
        has_driver_license=True,
        speaks_deutsch=False,
        speaks_english=True,
        speaks_french=False,
        speaks_esperanto=True,
        speaks_latin=False,
        favorite_color='Blue',
    )
    filler = PdfFormFiller(pdf_template=template)
    filler.fill()

    return filler


# python -m backend.credo.brokerage.outputs._pdffiller.tests.integration.test_integration
if __name__ == '__main__':
    filled_filler = test_pdf_full_fill()
    filled_filler.utility.convert()
    # print(filled_filler.utility.describe_form_fields())
    filled_filler.write('test.pdf')
