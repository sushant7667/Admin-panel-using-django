from django.db import models
# from countrytask.models import countrymodel,statemodel
from django.db.models.deletion import CASCADE
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models

#country state
class countrymodel(models.Model):
    cname = models.CharField(max_length = 50,null=True)

    # def __str__(self):
    #     return self.cname
    

class statemodel(models.Model):
    country_id= models.ForeignKey(countrymodel, on_delete=models.CASCADE)
    sname = models.CharField(max_length = 50,null=True)

    def __str__(self):
        return self.sname

# emp master
class useremp(models.Model):   

    Firstname = models.CharField(max_length=255,null=True)
    Lastname = models.CharField(max_length=255,null=True)
    mobile_no = models.CharField(max_length=255,null=True)
    choices = (('male','male'),('female','female'))
    gender = models.CharField(max_length=50,choices=choices,default = 'male')
    email = models.CharField(max_length=255,null=True,unique=True)
    countryId = models.ForeignKey(countrymodel, on_delete=models.CASCADE,null=True)
    stateId = models.ForeignKey(statemodel, on_delete=models.CASCADE,null=True)
    isactive  = models.BooleanField(default=True)


#role master
class role(models.Model):
    rolename = models.CharField(max_length = 50,null=True)
    isactive = models.BooleanField(default=True)

#Usermaster

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user



    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class usermaster(AbstractBaseUser,PermissionsMixin):
    Name = models.CharField(max_length = 250,null=True)
    role_id = models.ForeignKey(role, on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=255,null=True,unique=True)
    number = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=250,null=True)
    # Image = models.ImageField(upload_to='static/media', blank=True, null=True,verbose_name='photo')

    isactive = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    

    def __str__(self):
        return self.email


class MenuItem(models.Model):
    MenuId = models.IntegerField(primary_key=True)
    MenuName = models.CharField(max_length=255,null=True)
    MenuDescription = models.CharField(max_length=255,null=True,blank=True)
    MenuPath = models.CharField(max_length=255,null=True,blank=True)
    MenuIcon = models.CharField(max_length=255,null=True,blank=True)
    ParentId = models.IntegerField(null=True,blank=True)
    MenuPostion = models.IntegerField(null=True,blank=True)
    SortOrder = models.IntegerField(null=True,blank=True)


class Permission(models.Model):
    Role_Id = models.ForeignKey(role, on_delete=models.CASCADE,null=True)
    checkbox_id = models.ManyToManyField(MenuItem)
