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

    def get_absolute_url(self):
        return reverse("propertyDetails", kwargs={"pk": self.pk})


class IssueCategory(models.Model):
    title = models.CharField(max_length=50)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("categories")


class Issue(models.Model):
    class StatusENUM(models.TextChoices):
        CRE = 'CREATED',
        ASS = 'ASSIGNED',
        PRO = 'IN_PROGRESS',
        COM = 'COMPLETED',
        DEL = 'DELETED',
        CLO = 'CLOSED'

    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=200, null=False, blank=False)

    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True)
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusENUM.choices, default=StatusENUM.CRE)
 
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name="assigned_by_issues_set")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name="assigned_to_issues_set")
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_issues_set")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("issueDetails", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-updated', '-created']
        

class Comment(models.Model):
    messageText = models.TextField(max_length=255, null=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="issue_comments")

    dateAdded = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['dateUpdated', 'dateAdded']

    def __str__(self):
        return f'{self.author.username}: {self.messageText}'