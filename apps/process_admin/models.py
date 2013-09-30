from django.db import models
from django.contrib.auth.models import User


class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).order_by('-date_modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CommonQueriesManager(GenericManager):
    
    def get_available(self):
        return self.filter(is_active=True, is_available=True).order_by('-date_modified')


class UserType(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_permissions(self):
        return ", ".join([s.name for s in self.permissions_set.all()])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('pk',)


class Permissions(models.Model):
    """Table to define all Permissions."""
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=300, verbose_name="description")
    usertype = models.ManyToManyField(UserType)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

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
        ordering = ('id',)


class UserProfile(models.Model):
    """Table necessary for create an user account, This serves to validate the email."""
    dni = models.CharField(max_length=30, verbose_name="dni")
    phone = models.CharField(max_length=150, verbose_name="phone")
    cell_phone = models.CharField(max_length=150, verbose_name="cell_phone")
    city = models.CharField(max_length=150, verbose_name="city")
    address = models.CharField(max_length=150, verbose_name="address")
    date_born = models.DateField(null=True)
    is_active_worker = models.BooleanField(default=True)

    user = models.OneToOneField(User)
    user_type = models.ForeignKey(UserType, null=True)
    employment = models.ForeignKey(Employments, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()

    def __unicode__(self):
        return "%s: %s %s" % (self.user, self.user_type, self.is_active)


class Activities(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    measuring_unit = models.CharField(max_length=50, verbose_name="measuring_unit")
    value = models.CharField(max_length=50, verbose_name="value")
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user')
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.code, self.name, self.value)

    def get_table_name(self):
        return "Actividades"


class LegalDiscounts(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    value = models.CharField(max_length=50, verbose_name="value")
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.code, self.name, self.value)


class GeneralDiscounts(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.code, self.name, self.value)
    

class Places(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.code, self.name, self.value)
    
    
class Tools(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.code, self.name, self.value)
    
    
    