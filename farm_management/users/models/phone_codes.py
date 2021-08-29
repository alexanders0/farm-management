"""Phone Code model."""

# Django
from django.db import models
import random

# Utilities
from farm_management.utils.models import FarmModel


class PhoneCode(FarmModel):
    """Phone Code model

    Phone codes to verify user phone number.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    phone_code = models.CharField(max_length=5, blank=True)
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its phone number.'
    )

    def __str__(self):
        """ Return user's str representation """
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.phone_code == '':
            number_list = [x for x in range(10)]
            code_items = []

            for i in range(5):
                num = random.choice(number_list)
                code_items.append(num)

            code_string = "".join(str(item) for item in code_items)
            self.phone_code = code_string
        super().save(*args, **kwargs)
