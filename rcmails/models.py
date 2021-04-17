from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone 


# a user with username='default' is mandatory to use it when deleting instances
def default_user():
    return User.objects.get(username='default').pk


class Departement(models.Model):
    abbreviation = models.CharField(max_length=10)
    english_name = models.CharField(blank=True, max_length=50)
    arabic_name = models.CharField(blank=True, max_length=50)
    location = models.URLField(blank=True, max_length=50)
    created = models.DateField(auto_now_add=True)
    # test_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('auth.User', related_name='created_departements', on_delete=models.SET_DEFAULT, default=default_user)

    def __str__(self):
        return self.abbreviation

    def get_absolute_url(self):
        return reverse('rcmails:departement_detail', kwargs={'pk': self.pk})
                     
    class Meta:
        ordering = ['-created']


class Cmail(models.Model):
    number = models.IntegerField()
    title = models.TextField()
    recieving_date = models.DateField(blank=True, null=True)
    source = models.ForeignKey(Departement, related_name='sended_cmails', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='created_cmails', on_delete=models.SET_DEFAULT, default=default_user)

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('rcmails:cmail_detail', kwargs={'pk': self.pk})
                     
    class Meta:
        ordering = ['-created']


