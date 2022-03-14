from asyncore import read
from dataclasses import fields
from inspect import classify_class_attrs
from statistics import mode
from tenant_mgmt.models import *
from rest_framework import serializers 


# class UserGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserGroup
#         fields = ['id', 'groupName']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','street', 'apartment', 'city', 'zipCode', 'country' ] 


class UserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'bio', 'groupId', 'residenceAddressId'] 
       


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ['id','name', 'ownerId', 'tenants' ] 
        # depth  = 2



class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = ['id','title'] 



class IssueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Issue
        fields = ['id', 'name','description', 'category', 'room', 'status','assignee','assigner', 'submitter'  ] 
        # depth = 3


class CommentsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Comment
        fields = ['id', 'messageText', 'issueId', 'authorId', ] 
        depth = 2

