import logging
import collections
from typing import Dict, Tuple, List, Set

from .exceptions import (
    RequiredPdfFieldMissing,
    PdfChoiceIncorrect,
    UnrecognizedTemplateKwarg
)
from .fields import (
    AbstractPdfFormField,
    RadioFormField,
    TotalFormField,
    form_function_field,
)


logger = logging.getLogger(__name__)


class PdfTemplateMeta(type):
    _ALL_DEFINED_PDF_FIELD_ATTRS_KEY = '_all_defined_pdf_field_attrs'
    _REQ_PDF_FORM_REPRS_KEY = '_req_pdf_form_reprs'
    _ALL_PDF_FORM_REPRS_KEY = '_all_pdf_form_reprs'

    # form_repr: (field, class_attr)
    _PDF_FIELD_CLASS_ATTR_PAIRS_BY_FORM_REPR_KEY = '_field_cls_attr_pairs_by_form_repr'
    # class_attr: (field, form_repr)
    _PDF_FIELD_FORM_REPR_PAIRS_BY_CLASS_ATTR_KEY = '_field_form_repr_pairs_by_cls_attr'

    @classmethod
    def _get_field_class_attr_pairs_by_form_repr(cls, bases, attrs=None) -> Dict[str, Tuple[AbstractPdfFormField, str]]:
        field_cls_attr_pairs_by_form_repr = collections.OrderedDict()
        # Get fields from inherited bases
        for base in bases:
            existing_fields = getattr(base, cls._PDF_FIELD_CLASS_ATTR_PAIRS_BY_FORM_REPR_KEY, collections.OrderedDict())
            field_cls_attr_pairs_by_form_repr.update(existing_fields)

        # Get fields from current class def
        attrs = attrs or collections.OrderedDict()
        for attr, value in attrs.items():
            if isinstance(value, AbstractPdfFormField):
                field_cls_attr_pairs_by_form_repr.update({value.form_repr or attr: (value, attr)})
            elif isinstance(value, form_function_field):
                field_cls_attr_pairs_by_form_repr.update({value.field.form_repr or attr: (value, attr)})

        return field_cls_attr_pairs_by_form_repr

    @classmethod
    def __prepare__(self, name, bases):
        # Preserve attr ordering to accept args in template init
        return collections.OrderedDict()

    def __new__(cls, name, bases, attrs):
        all_form_reprs = set()
        required_form_reprs = set()
        cls_attrs = list()
        field_cls_attr_pairs_by_form_repr = cls._get_field_class_attr_pairs_by_form_repr(bases, attrs)
        field_form_repr_pairs_by_cls_attr = {}
        for form_repr, cls_attr_pair in field_cls_attr_pairs_by_form_repr.items():
            field, cls_attr = cls_attr_pair
            field_form_repr_pairs_by_cls_attr[cls_attr] = (field, form_repr)
            if field.required:
                required_form_reprs.add(form_repr)
            cls_attrs.append(cls_attr)
            all_form_reprs.add(form_repr)

        attrs[cls._ALL_DEFINED_PDF_FIELD_ATTRS_KEY] = cls_attrs
        attrs[cls._ALL_PDF_FORM_REPRS_KEY] = all_form_reprs
        attrs[cls._REQ_PDF_FORM_REPRS_KEY] = required_form_reprs
        attrs[cls._PDF_FIELD_FORM_REPR_PAIRS_BY_CLASS_ATTR_KEY] = field_form_repr_pairs_by_cls_attr
        attrs[cls._PDF_FIELD_CLASS_ATTR_PAIRS_BY_FORM_REPR_KEY] = field_cls_attr_pairs_by_form_repr

        return super(PdfTemplateMeta, cls).__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        # For instances of a template, we dont want attribute values to be
        # their defined field type. We want to set them to the passed in value,
        # or None.
        template_obj = super().__call__(*args, **kwargs)
        for def_field in getattr(template_obj, cls._ALL_DEFINED_PDF_FIELD_ATTRS_KEY):
            value = getattr(template_obj, def_field, None)
            if isinstance(value, AbstractPdfFormField):
                setattr(template_obj, def_field, None)

        return template_obj


class PdfFormTemplate(metaclass=PdfTemplateMeta):
    def __init__(self, *args, **kwargs):
        # set instance attributes from args, order is important here
        for i, arg in enumerate(args):
            setattr(self, self._all_cls_attrs[i], arg)

        # set instance attributes from kwargs
        for key, value in kwargs.items():
            # @TODO Validate we cant set calculated field values
            if key not in self._all_cls_attrs:
                raise UnrecognizedTemplateKwarg(f'Unrecognized template kwarg `{key}`')
            setattr(self, key, value)

        self._form_repr_value_store = {}
        # Tracks whether fields have been calculated and finalized
        self._prepared = False

    def __setattr__(self, key, value):
        if getattr(self, '_prepared', False):
            raise AttributeError('Setting attributed on prepared template is forbidden')

        return object.__setattr__(self, key, value)

    @property
    def _all_cls_attrs(self) -> List[str]:
        return getattr(self, PdfTemplateMeta._ALL_DEFINED_PDF_FIELD_ATTRS_KEY)

    @property
    def _field_cls_attr_pairs_by_form_repr(self) -> dict:
        # Type hinting/testable accessing for attrs "magically" set in meta
        return getattr(self, PdfTemplateMeta._PDF_FIELD_CLASS_ATTR_PAIRS_BY_FORM_REPR_KEY)

    # @TODO
    @property
    def _field_form_repr_pairs_by_cls_attr(self) -> dict:
        # Type hinting/testable accessing for attrs "magically" set in meta
        return getattr(self, PdfTemplateMeta._PDF_FIELD_FORM_REPR_PAIRS_BY_CLASS_ATTR_KEY)

    @property
    def _form_reprs(self) -> Set[str]:
        # Type hinting/testable accessing for attrs "magically" set in meta
        return getattr(self, PdfTemplateMeta._ALL_PDF_FORM_REPRS_KEY)

    @property
    def _required_form_reprs(self) -> Set[str]:
        # Type hinting/testable accessing for attrs "magically" set in meta
        return getattr(self, PdfTemplateMeta._REQ_PDF_FORM_REPRS_KEY)

    def prepare(self) -> "PdfFormTemplate":
        """
        Called by PdfFiller before filling.
        - Validates
        - Builds a map of form_repr to values
        - Calculates function fields
        """
        # Build map from form_rep to field, value
        self._calc_form_repr_values()
        self._validate()

        return self

    def get(self, attr):
        """
        Gets field value after being prepared for given attr
        """
        if not self._prepared:
            raise ValueError('Template must be prepared to use `get`')
        try:
            field, form_repr = self._field_form_repr_pairs_by_cls_attr[attr]
        except KeyError:
            raise AttributeError(f'{attr} undefined on {self}')

        return self._form_repr_value_store.get(form_repr, None)

    def _calc_form_repr_values(self):
        for form_repr in self._form_reprs:
            if form_repr not in self._form_repr_value_store:
                self._calc_value_for_form_repr(form_repr)

    def _calc_value_for_form_repr(self, form_repr: str):
        field, cls_attr = self._field_cls_attr_pairs_by_form_repr[form_repr]
        value = getattr(self, cls_attr, None)
        if isinstance(field, form_function_field):
            func_field = value
            value = func_field()

        elif isinstance(field, TotalFormField):
            child_values = []
            for child_form_repr in field.child_form_reprs:
                child_value = self._calc_value_for_form_repr(child_form_repr)
                if child_value:
                    child_values.append(child_value)

            value = sum(child_values)

        self._form_repr_value_store[form_repr] = value
        return value

    def _validate(self):
        self._validate_required_form_reprs()
        self._validate_choice_fields()
        self.validate()

    def _validate_required_form_reprs(self):
        for req_form_repr in self._required_form_reprs:
            value = self._form_repr_value_store.get(req_form_repr)
            if value is None:
                raise RequiredPdfFieldMissing(f'Missing required field value for `{req_form_repr}`')

    def _validate_choice_fields(self):
        for form_repr in self._form_reprs:
            field, value = self.get_field_value_pair_for_form_repr(form_repr)
            if isinstance(field, RadioFormField):
                if value is not None and value not in field.choices:
                    raise PdfChoiceIncorrect(f'Incorrect choice provided `{value}` for form_repr `{form_repr}`')

    def validate(self):
        """
        Hook for extra validation post build should raise
        if validation fails.
        """
        pass

    def get_field_value_pair_for_form_repr(self, form_repr: str) -> Tuple[AbstractPdfFormField, any]:
        """
        Called by `PdfFiller` to get PdfField based on form_repr str
        """
        # Set inside metaclass
        field, _ = self._field_cls_attr_pairs_by_form_repr[form_repr]
        value = self._form_repr_value_store.get(form_repr)
        return field, value

    def get_pdf_template(self):
        """
        Implemented by concrete
        """
        raise NotImplementedError("Must implement get_pdf_template")

    def get_pdf_file_name(self):
        """
        Implemented by concrete
        """
        raise NotImplementedError("Must implement get_pdf_file_name")
