from django.db import models
from django.contrib.auth.models import User
from tenant_mgmt.models import Address


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="address_users_set", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    def __str__(self):
        return f'{self.user.username} Profile'