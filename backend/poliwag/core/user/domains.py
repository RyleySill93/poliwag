import datetime
import decimal
import enum
from typing import Optional
from pydantic import constr
from poliwag.common.nanoid import NanoIdType
from poliwag.common.base_domains import BaseDomain
from poliwag.common.identity.constants import StatesEnum
from poliwag.core.user.constants import OnboardingStatusEnum, EmploymentStatusEnum, NetWorthEnum


class UserDomain(BaseDomain):
    id: NanoIdType
    email: str
    phone: str
    is_active: Optional[bool] = False
    is_staff: Optional[bool] = False

    # Profile
    first_name: str
    last_name: str
    legal_first_name: Optional[str] = None
    legal_last_name: Optional[str] = None
    street_address: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    birthday: Optional[datetime.date] = None
    ssn_mask: Optional[str] = None
    onboarding_status: Optional[OnboardingStatusEnum] = None
    persona_inquiry_id: Optional[str] = None

    employment_status: Optional[EmploymentStatusEnum] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    gross_income_current_year: Optional[decimal.Decimal] = None
    gross_income_previous_year: Optional[decimal.Decimal] = None
    estimated_net_worth: Optional[NetWorthEnum] = None

    is_associated_with_securities_industry: Optional[bool] = None
    is_public_company_controller: Optional[bool] = None
    is_senior_government_official: Optional[bool] = None

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_legal_name(self):
        return f"{self.legal_first_name} {self.legal_last_name}"

    @property
    def full_address(self):
        return f"{self.street_address} {self.city}, {self.state} {self.zipcode}"
    def to_dict(self):
        return {
            'full_name': self.full_name,
            'full_legal_name': self.full_legal_name,
            **self.dict(),
        }


class UserProfileDomain(BaseDomain):
    user_id: NanoIdType
    first_name: Optional[constr(max_length=40, strip_whitespace=True)] = None
    last_name: Optional[constr(max_length=40, strip_whitespace=True)] = None
    legal_first_name: Optional[constr(max_length=40, strip_whitespace=True)] = None
    legal_last_name: Optional[constr(max_length=40, strip_whitespace=True)] = None
    birthday: Optional[datetime.date] = None
    citizenship_country_code: Optional[constr(min_length=2, max_length=2)] = None
    ssn: Optional[constr(min_length=9, max_length=9, strip_whitespace=True)] = None
    street_address: Optional[constr(max_length=100, strip_whitespace=True)] = None
    city: Optional[constr(max_length=40, strip_whitespace=True)] = None
    state: Optional[StatesEnum] = None
    zipcode: Optional[constr(min_length=5, max_length=20, strip_whitespace=True)] = None
    onboarding_status: Optional[OnboardingStatusEnum] = None
    persona_inquiry_id: Optional[str] = None

    employment_status: Optional[EmploymentStatusEnum] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    gross_income_current_year: Optional[decimal.Decimal] = None
    gross_income_previous_year: Optional[decimal.Decimal] = None
    estimated_net_worth: Optional[NetWorthEnum] = None

    is_associated_with_securities_industry: Optional[bool] = None
    is_public_company_controller: Optional[bool] = None
    is_senior_government_official: Optional[bool] = None


class UpdateProfileFieldEnum(str, enum.Enum):
    """
    Fields eligible to be updated for userprofile
    """
    BIRTHDAY = "birthday"
    CITIZENSHIP_COUNTRY_CODE = "citizenship_country_code"
    SSN = "ssn"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    LEGAL_FIRST_NAME = "legal_first_name"
    LEGAL_LAST_NAME = "legal_last_name"
    STREET_ADDRESS = "street_address"
    CITY = "city"
    STATE = "state"
    ZIPCODE = "zipcode"
    PERSONA_INQUIRY_ID = "persona_inquiry_id"

    EMPLOYMENT_STATUS = 'employment_status'
    OCCUPATION = 'occupation'
    EMPLOYER = 'employer'
    GROSS_INCOME_CURRENT_YEAR = 'gross_income_current_year'
    GROSS_INCOME_PREVIOUS_YEAR = 'gross_income_previous_year'
    ESTIMATED_NET_WORTH = 'estimated_net_worth'

    IS_ASSOCIATED_WITH_SECURITIES_INDUSTRY = 'is_associated_with_securities_industry'
    IS_PUBLIC_COMPANY_CONTROLLER = 'is_public_company_controller'
    IS_SENIOR_GOVERNMENT_OFFICIAL = 'is_senior_government_official'
