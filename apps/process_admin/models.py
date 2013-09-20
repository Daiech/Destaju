from django.db import models
from django.contrib.auth.models import User

class UserProfileManager(models.Manager):

    def create_user_profile(self):
        pass


class ActivitiesManager(models.Manager):
    
    def get_available(self):
        return self.filter(is_active=True, is_available=True).order_by('-date_modified')
    
    def get_active(self):
        return self.filter(is_active=True).order_by('-date_modified')


class UserType(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = UserTypeManager()

    def get_permissions(self):
        return ", ".join([s.name for s in self.permissions_set.all()])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Permissions(models.Model):
    """Table to define all Permissions."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")
    usertype = models.ManyToManyField(UserType)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = UserTypeManager()

    def __unicode__(self):
        return self.name

    def user_types(self):
        return ", ".join([s.name for s in self.usertype.all()])

    class Meta:
        ordering = ('name',)


class Employments(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = EmploymentManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


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
    id_user_type = models.ForeignKey(UserType)
    id_employment = models.ForeignKey(Employments, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # objects = UserProfileManager()

    # def __unicode__(self):
    #     return "%s: %s %s" % (self.id_user, self.id_user_type, self.is_active)


class Activities(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    measuring_unit = models.CharField(max_length=50, verbose_name="measuring_unit")
    value = models.CharField(max_length=50, verbose_name="value")
    id_user = models.ForeignKey(
        User,  null=False, related_name='%(class)s_id_user') 
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = ActivitiesManager()
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.code, self.name, self.value)

