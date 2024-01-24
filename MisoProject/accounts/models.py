from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


 
class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')
    
    
class Use_Miso(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='use_miso_images/')    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Used_Miso(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='used_miso_images/')
    thoughts = models.TextField()
    taste_rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])
    appearance_rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])
    timestamp = models.DateTimeField(auto_now_add=True)
    used_miso = models.BooleanField(default=False)
    # favorites = models.ManyToManyField(User, related_name='favorite_used_misos', blank=True)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_used_misos', blank=True)
   
   
    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')




