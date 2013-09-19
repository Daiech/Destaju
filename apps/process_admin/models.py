from django.db import models
from django.contrib.auth.models import User

class UserProfileManager(models.Manager):

    def create_user_profile(self):
        pass


class UserType(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = UserTypeManager()

    def __unicode__(self):
        return self.name, self.is_active


class Employment(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = EmploymentManager()

    def __unicode__(self):
        return self.name, self.is_active


class UserProfile(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    dni = models.CharField(max_length=30, verbose_name="dni")
    phone = models.CharField(max_length=150, verbose_name="phone")
    cell_phone = models.CharField(max_length=150, verbose_name="cell_phone")
    city = models.CharField(max_length=150, verbose_name="city")
    address = models.CharField(max_length=150, verbose_name="address")
    date_born = models.DateField()
    is_active_worker = models.BooleanField(default=True)

    id_user = models.OneToOneField(User)
    id_user_type = models.OneToOneField(UserType)
    id_employment = models.OneToOneField(Employment)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = UserProfileManager()

    def __unicode__(self):
        return "%s: dni:%s, user type:%s" % (self.id_user, self.dni, self.id_user_type)
