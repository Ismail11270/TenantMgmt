from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone
from django.urls import reverse

class Address(models.Model):
    street = models.CharField(max_length=50, null=False)
    apartment = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=50, null=False)
    zipCode = models.CharField(max_length=15, null=False)
    country = models.CharField(max_length=50, null=False)  
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.country} {self.zipCode} {self.city} , {self.street} {self.apartment}'

    def get_absolute_url(self):
        return reverse("addressDetails", kwargs={"pk": self.pk})
    

class Property(models.Model):
    name = models.CharField(max_length=50, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name="address_properties_set")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="owner_property_set", null=True, blank=True)
    tenants = models.ManyToManyField(User, related_name="tenant_property_set", blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name


class IssueCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Issue(models.Model):
    class StatusENUM(models.TextChoices):
        CREATED = 'CRE',
        ASSIGED = 'ASS'
        PROGRESS = 'PRO'
        COMPLATED = 'COM'
        DELETED = 'DEL'
        CLOSED = 'CLO'

    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=200, null=True)

    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True)
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=StatusENUM.choices, default=StatusENUM.CREATED)

    assigner = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name="assigned_by_issues_set")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name="assigned_to_issues_set")
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_issues_set")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-updated', '-created']
        

class Comments(models.Model):
    messageText = models.TextField(max_length=200, null=True)

    authorId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    issueId = models.ForeignKey(Issue, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']