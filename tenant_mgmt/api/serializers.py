from tenant_mgmt.models import Address, Property, IssueCategory, Issue, Comment
from users.models import Profile
from rest_framework import serializers 


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'apartment', 'city', 'zipCode', 'country', 'dateAdded'] 


class UserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'address'] 


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ['id', 'name', 'address', 'owner', 'owner', 'dateAdded'] 
        # depth  = 2


class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = ['id', 'title', 'dateAdded'] 


class IssueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'category', 'related_property', 'status', 'manager', 'assignee', 'submitter', 'created', 'updated'] 
        # depth = 3


class CommentsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Comment
        fields = ['id', 'messageText', 'author', 'issue', 'dateAdded', 'dateUpdated'] 
        depth = 2

