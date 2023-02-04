from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import datetime
import uuid
# Create your models here.

GENDER_CHOICES =(
    ('male','male'),
    ('female','female'),
)


class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,mobile,password =None):
        if not email:
            raise ValueError('User must have an email address')

        if not mobile :
            raise ValueError('User must have mobile')

        user =self.model(
            email  = self.normalize_email(email),
            mobile = mobile,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_vendor(self,first_name,mobile,email,gst_no,password=None):
        if not email:
            raise ValueError('vendor must have an email address')

        vendor = self.model(
            email =self.normalize_email(email),
            mobile=mobile,
            first_name=first_name,
            gst_no=gst_no,
            
        )
        vendor.is_admin = False
        vendor.is_active = True
        vendor.is_verified = False
        vendor.is_staff = True
        vendor.is_superadmin = False
        vendor.set_password(password)
        vendor.save(using=self._db)
        return vendor

    
    def create_superuser(self,email,first_name,last_name,mobile,password):
        user = self.create_user(
            email=self.normalize_email(email),
            mobile=mobile,
            first_name= first_name,
            last_name=last_name,
            password=password,
    
        )
        user.is_admin =True
        user.is_active = True
        user.is_staff =True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

    

class myuser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    mobile = models.CharField(max_length=15,null=True)
    DP  =  models.ImageField(blank=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,null=True,blank=False)


    gst_no = models.CharField(max_length=8,unique=True,null=True)
    
    forgot_password_token = models.CharField(max_length=100,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login =  models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin =models.BooleanField(default=False)
    is_active =models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile']
    objects = MyAccountManager()


    def __str__(self) :
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    


class Userdetail(models.Model):
          
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        email = models.EmailField(max_length=100,unique=True)
        mobile = models.CharField(max_length=15,null=True)
        
        addressline1 = models.CharField(max_length=300)
        addressline2 = models.CharField(max_length=300)
        city =models.CharField(max_length=100)
        state = models.CharField(max_length=100)
        country = models.CharField(max_length=100)
        user_id = models.ForeignKey(myuser,on_delete=models.CASCADE)

        default = models.BooleanField(default=False)

        def __str__(self) :
            return self.first_name
        

   
