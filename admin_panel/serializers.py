from rest_framework import serializers
from .views import User

class UserAdminViewSeirailzers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields ='__all__'


