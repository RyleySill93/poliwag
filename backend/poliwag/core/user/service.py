import logging
from typing import List, Optional
from poliwag.common.nanoid import NanoIdType
from poliwag.core.user.domains import UserDomain, UserProfileDomain, UpdateProfileFieldEnum
from poliwag.core.user.models import UserProfile
from poliwag.common.identity.service import IdentityService
from poliwag.common.identity.domains import IdentityDomain


logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        identity_service: Optional[IdentityService] = None,
    ):
        self.identity_service = identity_service or IdentityService.factory()

    @classmethod
    def factory(cls) -> "UserService":
        return cls(
            identity_service=IdentityService.factory(),
        )

    def create(self, user: UserDomain) -> UserDomain:
        # Create user
        identity = IdentityDomain(
            id=user.id,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active,
            is_staff=user.is_staff,
        )
        self.identity_service.create(identity)

        # Create profile
        UserProfile.objects.create(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        return self.get_by_id(user_id=user.id)

    def update_profile(self, user_profile: UserProfileDomain, fields: List[UpdateProfileFieldEnum]) -> UserDomain:
        update_kwargs = {}
        # Only update fields specified
        for field in fields:
            update_kwargs[field.value] = getattr(user_profile, field)

        UserProfile.objects.filter(user_id=user_profile.user_id).update(**update_kwargs)

        return self.get_by_id(user_id=user_profile.user_id)

    def get_by_id(self, user_id: NanoIdType) -> UserDomain:
        user = self.identity_service.get_by_id(user_id)

        user_profile = UserProfile.objects.get(user_id=user_id)

        return UserDomain(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            legal_first_name=user_profile.legal_first_name,
            legal_last_name=user_profile.legal_last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            street_address=user_profile.street_address,
            city=user_profile.city,
            state=user_profile.state,
            zipcode=user_profile.zipcode,
            birthday=user_profile.birthday,
            ssn_mask=f"*****{user_profile.ssn[-4:]}" if user_profile.ssn else None,
            onboarding_status=user_profile.onboarding_status,
            persona_inquiry_id=user_profile.persona_inquiry_id,
            employment_status=user_profile.employment_status,
            occupation=user_profile.occupation,
            employer=user_profile.employer,
            gross_income_current_year=user_profile.gross_income_current_year,
            gross_income_previous_year=user_profile.gross_income_previous_year,
            estimated_net_worth=user_profile.estimated_net_worth,
            is_associated_with_securities_industry=user_profile.is_associated_with_securities_industry,
            is_public_company_controller=user_profile.is_public_company_controller,
            is_senior_government_official=user_profile.is_senior_government_official,
        )

    def get_user_profile_by_user_id(self, user_id: NanoIdType) -> UserProfileDomain:
        user_profile = UserProfile.objects.get(user_id=user_id)

        return UserProfileDomain(
            user_id=user_profile.user_id,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            birthday=user_profile.birthday,
            citizenship_country_code=user_profile.citizenship_country_code,
            ssn=user_profile.ssn,
            street_address=user_profile.street_address,
            city=user_profile.city,
            state=user_profile.state,
            zipcode=user_profile.zipcode,
        )