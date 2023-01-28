import decimal
from decimal import Decimal
from collections import defaultdict
from dateutil import parser as date_parser
import datetime
import operator
from itertools import islice
from importlib import import_module
from typing import Union, Iterable, TypeVar, List, Callable, Optional

from django.urls import reverse
from django.utils.functional import SimpleLazyObject, new_method_proxy
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    format_number,
    is_valid_number,
    parse as parse_phone_number,
)
from poliwag.settings import API_DOMAIN_NAME


def decimal_parse(number: Union[str, Decimal, float, int]) -> Decimal:
    """
    Ensures a decimal is returned with valid string or datetime
    """
    if isinstance(number, Decimal):
        return number

    if isinstance(number, float) or isinstance(number, int):
        return Decimal(number)

    return Decimal(number.replace(",", ""))


def safe_decimal_parse(number: Union[str, Decimal, None]) -> Optional[Decimal]:
    """
    Ensures a decimal is returned with valid string or datetime
    and does not raise for None
    """
    if not number:
        return None

    return decimal_parse(number)


def safe_datetime_parse(
    dt: Union[str, datetime.datetime, None],
) -> Optional[datetime.datetime]:
    """
    Ensures a datetime is returned with valid string or datetime
    and does not raise for None
    """
    if isinstance(dt, datetime.datetime):
        return dt

    if not dt:
        return None
    
    return date_parser.parse(dt)


def full_reverse(name: str, kwargs: dict):
    url = reverse(name, kwargs=kwargs)
    return f"{API_DOMAIN_NAME}{url}"


def raise_exception(exc: Exception):
    """
    Useful for lambdas
    """
    raise exc


_T = TypeVar("_T")


def split_every(iterable: Iterable[_T], split_size: int) -> List[_T]:
    piece: _T = list(islice(iterable, split_size))
    while piece:
        yield piece
        piece = list(islice(iterable, split_size))


def import_dotted_path_string(dotted_path: str):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            f"Module {module_path} does not define a {class_name} attribute/class"
        ) from err


def get_nested_attr(element: object, attribute: str):
    attributes = attribute.split(".")

    current_element = element
    for attribute in attributes:
        if not current_element:
            return None
        current_element = getattr(current_element, attribute)

    return current_element


def group_iterable_by_attribute(iterable: Iterable[object], attribute: str):
    grouped_iterable = defaultdict(list)

    for element in iterable:
        value = get_nested_attr(element, attribute)
        grouped_iterable[value].append(element)

    return grouped_iterable


def get_nested_key(element: object, attribute: str):
    attributes = attribute.split(".")

    current_element = element
    for attribute in attributes:
        if not current_element:
            return None
        current_element = current_element[attribute]

    return current_element


def legal_strftime(date: datetime.date) -> str:
    """
    Used for contracts formats dates to like '29th of July, 2022'
    """
    suffix = (
        "th"
        if 11 <= date.day <= 13
        else {1: "st", 2: "nd", 3: "rd"}.get(date.day % 10, "th")
    )
    return date.strftime("{S} of %B, %Y").replace("{S}", str(date.day) + suffix)


def format_money(number: decimal.Decimal) -> str:
    return f'${number:,.2f}'


def format_boolean(value: bool) -> str:
    if not value:
        return 'No'

    return 'Yes'


class _LazyReference(SimpleLazyObject):
    # These operators aren't included by default
    __le__ = new_method_proxy(operator.le)
    __ge__ = new_method_proxy(operator.ge)


def make_lazy(func: Callable) -> _LazyReference:
    """
    Func will not be executed unless accessed
    """
    return _LazyReference(func)


def slugify_phone_number(phone: str):
    try:
        n = parse_phone_number(phone, 'US')
    except NumberParseException as e:
        raise ValueError('Invalid phone number') from e

    if not is_valid_number(n):
        raise ValueError('Invalid phone number')

    return format_number(n, PhoneNumberFormat.E164)
