from django.db import models


class UserQuerySet(models.QuerySet):
    def for_ids(self, ids):
        return self.filter(id__in=ids)
