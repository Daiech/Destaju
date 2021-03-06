from django.db import models
from django.contrib.auth.models import User


class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).distinct().order_by('-date_added')

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
    objects = GenericManager()

    def can_login(self):
        if self.permissions_set.filter(code="AD_US_LOGIN").count() == 0:
            return False
        else:
            return True

    def can_admin(self):
        if self.pk == 1 or self.pk == 2:
            return True
        else:
            return False

    def can_generate_op(self):
        if self.pk == 1 or self.pk == 2 or self.pk == 3 or self.pk == 4:
            return True
        else:
            return False

    def can_fill_op(self):
        if self.pk == 1 or self.pk == 2 or self.pk == 3 or self.pk == 4:
            return True
        else:
            return False

    def can_rate_op(self):
        if self.pk == 1 or self.pk == 2 or self.pk == 3:
            return True
        else:
            return False

    def can_view_op(self):
        if self.pk == 1 or self.pk == 2 or self.pk == 6:
            return True
        else:
            return False

    def can_view_modifications(self):
        if self.pk == 1 or self.pk == 2 or self.pk == 6:
            return True
        else:
            return False

    def can_admin_inventory(self):
        if self.pk == 1 or self.pk == 2 or self.pk == 9:
            return True
        else:
            return False

    def can_admin_op(self):
        if self.pk in [1,2,3,4,6]:
            return True
        else:
            return False

    def get_permissions(self):
        return ", ".join([s.code for s in self.permissions_set.all()])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('pk',)


class Permissions(models.Model):
    """Table to define all Permissions."""
    code = models.CharField(max_length=150, verbose_name="code")
    description = models.CharField(max_length=300, verbose_name="description")
    usertype = models.ManyToManyField(UserType)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()

    def __unicode__(self):
        return self.code

    def user_types(self):
        return ", ".join([str(s) for s in self.usertype.all()])

    class Meta:
        ordering = ('code',)


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
    dni = models.CharField(max_length=30, null=False, verbose_name="dni")
    phone = models.CharField(max_length=150, verbose_name="phone")
    cell_phone = models.CharField(max_length=150, verbose_name="cell_phone")
    city = models.CharField(max_length=150, verbose_name="city")
    address = models.CharField(max_length=150, verbose_name="address")
    date_born = models.DateField(null=True, blank=True)
    is_active_worker = models.BooleanField(default=True)

    user = models.OneToOneField(User)
    user_type = models.ForeignKey(UserType, null=True)
    employment = models.ForeignKey(Employments, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()

    def get_permissions(self):
        return self.user_type.get_permissions()

    def __unicode__(self):
        return u"%s: %s %s" % (self.user, self.user_type, self.is_active)

    class Meta:
        ordering = ('is_active',)
        unique_together = ("user", "dni")
            

class Activities(models.Model):
    code = models.CharField(max_length=30,  verbose_name="code", unique=True)
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    measuring_unit = models.CharField(max_length=50, verbose_name="measuring_unit")
    value = models.IntegerField(max_length=50, verbose_name="value")
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user')
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.code, self.name)

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
        return "%s - %s" % (self.code, self.name)
    
    def get_table_name(self):
        return "Descuentos legales"


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
        return "%s - %s" % (self.code, self.name)
    
    def get_table_name(self):
        return "Descuentos Generales"
    

class Increases(models.Model):
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
        return "%s - %s" % (self.code, self.name)
    
    def get_table_name(self):
        return "Descuentos Generales"

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
        return "%s - %s" % (self.code, self.name)
    
    def get_table_name(self):
        return "Lugares"
    
    
class Tools(models.Model):
    code = models.CharField(max_length=30, verbose_name="code")
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    modifications = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = CommonQueriesManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.code, self.name)
    
    def get_table_name(self):
        return "Herramientas"
