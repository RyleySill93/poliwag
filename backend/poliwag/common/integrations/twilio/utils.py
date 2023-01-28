from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    format_number,
    is_valid_number,
    parse as parse_phone_number,
)


def format_phone_number_e164(phone: str) -> str:
    try:
        n = parse_phone_number(phone, 'US')
    except NumberParseException as e:
        raise ValueError('Invalid phone number') from e

    if not is_valid_number(n):
        raise ValueError('Invalid phone number')

    return format_number(n, PhoneNumberFormat.E164)
