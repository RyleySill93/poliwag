import enum


class OnboardingStatusEnum(str, enum.Enum):
    ACCOUNT_DETAILS = "ACCOUNT_DETAILS"
    ABOUT_YOU = "ABOUT_YOU"
    SUITABILITY = "SUITABILITY"
    COMPLIANCE = "COMPLIANCE"
    OPEN_YOUR_ACCOUNT = "OPEN_YOUR_ACCOUNT"
    TRANSFER_SHARES = "TRANSFER_SHARES"


ONBOARDING_STATUS_CHOICES = [
    (onboarding_status.value, onboarding_status.value)
    for onboarding_status in OnboardingStatusEnum
]


class EmploymentStatusEnum(str, enum.Enum):
    FULL_TIME = 'FULL_TIME'
    PART_TIME = 'PART_TIME'
    SELF_EMPLOYED = 'SELF_EMPLOYED'
    RETIRED = 'RETIRED'
    NOT_EMPLOYED = 'NOT_EMPLOYED'


EMPLOYMENT_STATUS_CHOICES = [
    (employment_status.value, employment_status.value)
    for employment_status in EmploymentStatusEnum
]


class NetWorthEnum(str, enum.Enum):
    UNDER_ONE_MILLION = "UNDER_ONE_MILLION"
    ONE_TO_TWO_MILLION = "ONE_TO_TWO_MILLION"
    TWO_TO_FIVE_MILLION = "TWO_TO_FIVE_MILLION"
    FIVE_TO_TEN_MILLION = "FIVE_TO_TEN_MILLION"
    OVER_TEN_MILLION = "OVER_TEN_MILLION"


NET_WORTH_CHOICES = [
    (option.value, option.value)
    for option in NetWorthEnum
]


class UserDocumentTypeEnum(str, enum.Enum):
    CUSTOMER_ID_FORM = "CUSTOMER_ID_FORM"


USER_DOCUMENT_TYPE_CHOICES = [
    (user_document_type.value, user_document_type.value)
    for user_document_type in UserDocumentTypeEnum
]
