import abc
import functools
from typing import List, Optional
import logging

import pdfrw

from .exceptions import ImproperlyFormattedRadioFormField


logger = logging.getLogger(__name__)


__all__ = [
    "TextFormField",
    "SelectFormField",
    "ToggleFormField",
    "TotalFormField",
    "RadioFormField",
    "form_function_field",
]


class AbstractPdfFormField(abc.ABC):
    # @TODO These cannot hold state because they are defined
    # as class level attributes...
    # 1) Go back to how things were (stateless fields) and hold values in templates ONLY
    # 2) Clone fields in metaclass new so each instance gets its own state
    # Either way I need somewhere to store value state I went down this path to be able
    # to recursively iterate through each field in case fields were dependent on others (TotalField).
    def __init__(self, form_repr: str=None, required=False):
        self.form_repr = form_repr
        self.required = required

    def __str__(self):
        return f'{self.__class__.__name__}(form_repr="{self.form_repr}", required={self.required})'

    def __repr__(self):
        return str(self)

    @abc.abstractmethod
    def fill(self, pdfrw_field, value):
        """
        All fields must implement this method.
        """
        ...


class TextFormField(AbstractPdfFormField):
    def fill(self, pdfrw_field, value):
        pdfrw_field.V = str(value)
        pdfrw_field.AP = str(value)


class ToggleFormField(AbstractPdfFormField):
    """
    Use for boxes, checks, etc that need to be toggled on or off
    based on a boolean value.
    """
    def fill(self, pdfrw_field, value: bool):
        if value:
            # More success here with '/Yes' vs '/On'
            value = pdfrw.PdfName('Yes')
        else:
            # Can be '/No'?
            value = pdfrw.PdfName('Off')

        pdfrw_field.V = value
        pdfrw_field.AP = value
        pdfrw_field.AS = value


class TotalFormField(TextFormField):
    def __init__(self, child_form_reprs: List[str], form_repr: str=None, required=False):
        self.child_form_reprs = child_form_reprs
        super().__init__(form_repr=form_repr, required=required)

    def __str__(self):
        return f'{self.__class__.__name__}(form_repr="{self.form_repr}", child_form_reprs={self.child_form_reprs}, required={self.required})'

class _FuncFormField:
    def __init__(self, func=None, field: Optional[AbstractPdfFormField]=None):
        field = field or TextFormField()
        functools.update_wrapper(self, func)
        if hasattr(func, '__call__'):
            self.func = func
            field.form_repr = func.__name__

        self.form_repr = field.form_repr or func.__name__
        self.required = False
        self.field = field

    def __get__(self, template, type=None):
        if template is None:
            return self
        return functools.partial(self, template)

    def __call__(self, *args, **kwargs):
        if not hasattr(self, 'func'):
            self.func = args[0]
            return self
        return self.func(*args, **kwargs)


form_function_field = _FuncFormField


class SelectFormField(AbstractPdfFormField):
    """
    Use for dropdown select field, the pdf type for these is checkbox
    """

    def __init__(self, choices: List[str], form_repr: str = None, required=False):
        self.choices = choices
        super().__init__(form_repr=form_repr, required=required)

    def __str__(self):
        return f'{self.__class__.__name__}(form_repr="{self.form_repr}", choices={self.choices}, required={self.required})'

    def fill(self, pdfrw_field, value: str):
        value = pdfrw.PdfName(value)
        pdfrw_field.V = value
        pdfrw_field.AP = value
        pdfrw_field.AS = value


class RadioFormField(SelectFormField):
    """
    Use when fields are correctly nested as children under a parent node.
    This would mean that each input box has the same parent reference.
    In forms, these feel like a group of toggles where only one can be
    selected.
    EG:
    '/T': '(Mortgage Applied For)'
        {'/N': {'/VA': (4, 0)}, '/D': {'/VA': (5, 0), '/Off': (6, 0)}}
        {'/N': {'/Conventional': (8, 0)}, '/D': {'/Conventional': (9, 0), '/Off': (10, 0)}}
        {'/N': {'/Other': (12, 0)}, '/D': {'/Other': (13, 0), '/Off': (14, 0)}}
        {'/N': {'/FHA': (16, 0)}, '/D': {'/Off': (17, 0), '/FHA': (18, 0)}}
        {'/N': {'/USDA/Rural Housing Service': (20, 0)}, '/D': {'/USDA/Rural Housing Service': (21, 0), '/Off': (22, 0)}}
    """

    def fill(self, pdfrw_field, value):
        kids = getattr(pdfrw_field, "Kids", None)
        if not kids:
            raise ImproperlyFormattedRadioFormField(f'{self} incorrectly formatted')

        for box in kids:
            # @TODO Enforce unique children names
            # Not all forms may have this in the ref Name
            ref_value = pdfrw.PdfName(value)
            # Match provided provided value to its field name
            if ref_value in box.AP.N.keys():
                # Set value
                # Mixed results using pdfrw.PdfName('On')
                # better results referencing the actual field name.
                # @TODO I may have to update AP here as well
                # box.AP = pdfrw.PdfName('On')
                box.AS = ref_value
                box.V = ref_value
                # Update parent nodes as well
                pdfrw_field.V = ref_value
                return

        # @TODO Raise for unknown values in checkbox...
        # Couldnt find the correct selector for provided value
