from rest_framework import serializers
from .models import *

class Countryserializer(serializers.ModelSerializer):
    class Meta:
        model = countrymodel
        fields = '__all__'

class Stateserializer(serializers.ModelSerializer):
    class Meta:
        model = statemodel
        fields = '__all__'

class userserializer(serializers.ModelSerializer):
    class Meta:
        model = useremp
        fields = '__all__'


class Roleserializer(serializers.ModelSerializer):
    class Meta:
        model = role
        fields = '__all__'

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = usermaster
        fields = '__all__'

class MenuIdserializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'