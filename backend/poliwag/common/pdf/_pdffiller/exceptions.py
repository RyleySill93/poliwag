from poliwag.common.exceptions import InternalException


# Base Exception
class PdfFillerException(InternalException):
    ...


# Template exceptions
class RequiredPdfFieldMissing(PdfFillerException):
    ...


class UnrecognizedTemplateKwarg(PdfFillerException):
    ...


class PdfChoiceIncorrect(PdfFillerException):
    ...


# Field exceptions
class ImproperlyFormattedRadioFormField(PdfFillerException):
    ...
