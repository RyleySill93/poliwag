import factory

from poliwag.common.identity.models import User
from poliwag.core.user.models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    is_active = True
    is_staff = False
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User

    @factory.post_generation
    def user_profile(self, create, extracted, **kwargs):
        if not create:
            return

        UserProfile.objects.create(
            user=self,
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            street_address=kwargs['street_address'],
            city=kwargs['city'],
            state=kwargs['state'],
            zipcode=kwargs['zipcode'],
            birthday=kwargs['birthday'],
            citizenship_country_code=kwargs['citizenship_country_code'],
            ssn=kwargs['ssn'],
        )
