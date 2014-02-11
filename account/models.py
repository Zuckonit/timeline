from django.db import models
from django.contrib.auth.models import User

from datetime import date

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name="account")
    sex  = models.IntegerField(default=2)  #0 is female, 1 is male 2 is unkown
    birthday = models.DateField(default=date(1990,1, 1))
    age  = models.IntegerField(default=0, editable=False)
    priority = models.IntegerField(default=1, editable=False)


    def save(self, *args, **kwargs):
        diff = date.today() - self.birthday
        if diff.days < 0:
            return super(UserProfile, self).save(*args, **kwargs)
        self.age = diff.days / 365
        return super(UserProfile, self).save(*args, **kwargs)
