from django.db import models
from poliwag.common.models import BaseModel
from poliwag.core.user.constants import (
    ONBOARDING_STATUS_CHOICES,
    OnboardingStatusEnum,
    EMPLOYMENT_STATUS_CHOICES,
    NET_WORTH_CHOICES,
    USER_DOCUMENT_TYPE_CHOICES,
)


class UserDocument(BaseModel):
    user = models.ForeignKey("identity.User", related_name='user_documents', on_delete=models.CASCADE)
    document = models.ForeignKey('documents.Document', related_name='user_documents', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=USER_DOCUMENT_TYPE_CHOICES)


class UserProfile(BaseModel):
    objects = models.Manager()

    user = models.OneToOneField(
        "identity.User",
        related_name="user_profile",
        on_delete=models.CASCADE,
    )
    onboarding_status = models.CharField(
        max_length=50,
        choices=ONBOARDING_STATUS_CHOICES,
        default=OnboardingStatusEnum.ACCOUNT_DETAILS,
        null=True,
        blank=True
    )
    persona_inquiry_id = models.CharField(max_length=50, null=True, blank=True)

    # about you
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    legal_first_name = models.CharField(max_length=40, null=True, blank=True)
    legal_last_name = models.CharField(max_length=40, null=True, blank=True)

    # account details
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    citizenship_country_code = models.CharField(max_length=3, null=True, blank=True)
    ssn = models.CharField(max_length=9, null=True, blank=True)

    # suitability
    employment_status = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_STATUS_CHOICES,
        null=True,
        blank=True
    )
    occupation = models.CharField(max_length=100, null=True, blank=True)
    employer = models.CharField(max_length=100, null=True, blank=True)
    gross_income_current_year = models.DecimalField(decimal_places=6, max_digits=25, null=True, blank=True)
    gross_income_previous_year = models.DecimalField(decimal_places=6, max_digits=25, null=True, blank=True)
    estimated_net_worth = models.CharField(
        max_length=50,
        choices=NET_WORTH_CHOICES,
        null=True,
        blank=True
    )

    # compliance
    is_associated_with_securities_industry = models.BooleanField(null=True, blank=True)
    is_public_company_controller = models.BooleanField(null=True, blank=True)
    is_senior_government_official = models.BooleanField(null=True, blank=True)
