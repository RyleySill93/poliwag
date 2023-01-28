import pytest
from unittest.mock import MagicMock

from ..._pdffiller import (
    fields,
    PdfFormTemplate,
)
from ..._pdffiller.exceptions import UnrecognizedTemplateKwarg, PdfChoiceIncorrect
from ..._pdffiller.templates import PdfTemplateMeta


class AttributesTemplateTest(PdfFormTemplate):
    required_number_1: int = fields.TextFormField(required=True)
    number_2: int = fields.TextFormField()
    random_field: str = fields.TextFormField(form_repr='number_3')
    checkbox_field: str = fields.RadioFormField(choices=['x', 'y'])
    total_field: int = fields.TotalFormField(child_form_reprs=['required_number_1', 'number_2', 'number_3'])
    dependent_total_field = fields.TotalFormField(child_form_reprs=['total_field', 'default_return_1'])

    @fields.form_function_field
    def default_return_1(self):
        return 1

    @fields.form_function_field
    def total_number_partial_decorator(self):
        return self.required_number_1 + (self.number_2 or 0)

    @fields.form_function_field(field=fields.TextFormField(form_repr='total_repr'))
    def total_number_full_decorator(self):
        return self.required_number_1 + (self.number_2 or 0)


# @TODO Test subclass implementations

class TestPdfFormTemplateMetaAttributes:
    """
    PdfFiller logic depends on these private attributes being
    set correctly by the meta class
    """
    def test_required_all_fields_correctly_mapped(self):
        all_form_reprs = getattr(AttributesTemplateTest, PdfTemplateMeta._ALL_PDF_FORM_REPRS_KEY)
        assert 'required_number_1' in all_form_reprs
        assert 'number_2' in all_form_reprs
        assert 'random_field' not in all_form_reprs
        # Form repr user defined
        assert 'number_3' in all_form_reprs

    def test_form_property_included_in_all_fields(self):
        all_form_reprs = getattr(AttributesTemplateTest, PdfTemplateMeta._ALL_PDF_FORM_REPRS_KEY)
        assert 'total_number_partial_decorator' in all_form_reprs
        assert 'total_repr' in all_form_reprs
        # Form repr user defined
        assert 'total_number_full_decorator' not in all_form_reprs

    def test_required_fields_correctly_mapped(self):
        req_form_reprs = getattr(AttributesTemplateTest, PdfTemplateMeta._REQ_PDF_FORM_REPRS_KEY)
        assert 'required_number_1' in req_form_reprs


class TestPdfFormTemplateConstruction:
    def test_raises_with_unrecognized_kwargs(self):
        with pytest.raises(UnrecognizedTemplateKwarg):
            AttributesTemplateTest(bad_kwarg=2)

    def test_undefined_get_template_raises_not_implemented(self):
        template = AttributesTemplateTest(required_number_1=2)
        with pytest.raises(NotImplementedError):
            template.get_pdf_template()


class TestPdfFormTemplatePrepare:
    def test_prepare_returns_self(self):
        template = AttributesTemplateTest(required_number_1=2)

        assert isinstance(template.prepare(), PdfFormTemplate)

    def test_prepare_calls_validation_hook(self):
        template = AttributesTemplateTest(required_number_1=2)
        template.validate = MagicMock()
        template.prepare()

        template.validate.assert_called_once()

    def test_prepares_correctly_with_args(self):
        template = AttributesTemplateTest(
            2,
            4,
        )
        template.prepare()
        assert template._form_repr_value_store['required_number_1'] == 2
        assert template._form_repr_value_store['number_2'] == 4
        assert template._form_repr_value_store['number_3'] == None

    def test_prepares_correctly_with_kwargs(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=4,
        )
        template.prepare()
        assert template._form_repr_value_store['required_number_1'] == 2
        assert template._form_repr_value_store['number_2'] == 4
        assert template._form_repr_value_store['number_3'] == None

    def test_form_repr_mapped_correctly(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=4,
            # This should be mapped to number_3 based on form_repr
            random_field=3,
        )
        template.prepare()
        assert template._form_repr_value_store['number_3'] == 3

    def test_form_function_without_args_prepares_correctly(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=4,
        )
        template.prepare()

        assert template._form_repr_value_store['total_number_partial_decorator'] == 6
        assert AttributesTemplateTest.total_number_partial_decorator.field.form_repr == 'total_number_partial_decorator'

    def test_form_function_with_args_prepares_correctly(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=4,
        )
        template.prepare()

        assert template._form_repr_value_store['total_repr'] == 6

    def test_checkbox_prepares_correctly(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=0,
            checkbox_field='x',
        )
        template.prepare()

        assert template._form_repr_value_store['checkbox_field'] == 'x'

    def test_checkbox_validation_raises_error_with_false_value(self):
        with pytest.raises(PdfChoiceIncorrect):
            template = AttributesTemplateTest(
                required_number_1=2,
                number_2=0,
                checkbox_field=False,
            )
            template.prepare()
        # assert template._form_repr_value_store['checkbox_field'] == 'x'

    def test_total_form_field_prepares_correctly(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=1,
            random_field=1,
        )
        template.prepare()
        assert template._form_repr_value_store['total_field'] == 4

    def test_total_form_field_with_dependent_prepares_correctly(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=1,
            random_field=1,
        )
        template.prepare()
        assert template._form_repr_value_store['dependent_total_field'] == 5

    def test_checkbox_raises_error_with_incorrect_value(self):
        template = AttributesTemplateTest(
            required_number_1=2,
            number_2=0,
            checkbox_field='bad_argument',
        )
        with pytest.raises(PdfChoiceIncorrect):
            template.prepare()
