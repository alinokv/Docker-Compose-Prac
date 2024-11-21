from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role_name = models.CharField(max_length=50)
    def __str__(self):
        return self.role_name

    
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,  blank=True, null=True)
    patronymic = models.CharField(max_length=30, blank=True)
    not_deleted = models.BooleanField(default=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
