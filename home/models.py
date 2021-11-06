from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import MyUserManager
from datetime import date


class User(AbstractBaseUser, PermissionsMixin):
    USERTYPE_CHOICES = (
        (1, 'ADMIN'),
        (2, 'STUDENT'),
    )

    password = models.CharField(max_length=500)
    email = models.EmailField('email address', unique=True,null=True,blank=True)
    first_name = models.CharField('first name', max_length=30, null=True, blank=True)
    last_name = models.CharField('last name', max_length=30, null=True, blank=True)
    dial_code = models.PositiveIntegerField('Dial code', default=91)
    image = models.ImageField(upload_to='userimages',null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    phone = models.PositiveBigIntegerField('Phone number', unique=True, null=True)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    user_type = models.IntegerField(choices=USERTYPE_CHOICES, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def calculateAge(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) <
            (self.dob.month, self.dob.day))
    
        return age

class Marks(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f'{self.student.get_full_name} {self.marks}'