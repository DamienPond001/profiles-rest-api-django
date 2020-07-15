from rest_framework import serializers

from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes User profile"""

    class Meta:
        #set up serializer to point to UserProfile model
        model = models.UserProfile

        #specify fields we want to manage
        fields = ('id', 'email', 'name', 'password')

        #specify how we want to be able to interact with ceryain fields
        #here we only want the password to be write only and be given type=password on the frontend
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    #We need to override the default update function to handle updating 
    #a password
    def update(self, instance, validated_data):
        """Handle updating user account"""
        #Check if password is to be updated
        if 'password' in validated_data:
            #get the new password and pop it off the dict to that the default
            #update method does not interact with it
            password = validated_data.pop('password')
            #hash and set the password for instance
            instance.set_password(password)
        
        #call the ModelSerializer update method to handle the rest of the input
        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializers profile feed items"""

    class Meta:
        model = models.ProfileFeedItem

        fields = ('id', 'user_profile', 'status_text', 'create_on')

        #Note that the id field is created by the Django ORM and that the created_on
        #fie;d is also automatically handled. These fields are therefore by defult set to 'read only'
        #We also want to make the user_profile field read only and to be automatically set
        #to the id of the authenticated user
        extra_kwargs = {
            'user_profile': {'read_only':True}
        }

