from django.db import models
from django.contrib.auth.models import User


class TimeLine(models.Model):
    user = models.ForeignKey(User, verbose_name="timeline")
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=2048)
    date_published = models.DateTimeField(auto_now=True)

    
    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        ordering = ['-date_published']


