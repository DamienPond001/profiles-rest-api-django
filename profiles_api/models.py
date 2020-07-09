from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('User Must have an email address')

        #HEre we normailse the mail i.e. make the second half of the email lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        #use django's standard password hashing function
        user.set_password(password)

        #Save new user using the defined database. This ensure that we support multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create new super user"""

        user = self.create_user(email, name, password)

        #Specify that the user is a superuser (part of PermissionMixin)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # We have to create Model manager for the objects, as this is needed to interact with the django CLI
    # This tells django ow to manage, create, etc new user objects
    objects = UserProfileManager()

    #We need to tell django that the new 'username' field has been changed to email
    USERNAME_FIELD = 'email'
    #Specify required fields (username is defult required)
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retirve fullname of user"""
        return self.name

    def get_short_name(self):
        """Retrive short name of user"""
        return self.name

    def __str___(self):
        """String represenation of the user"""
        return "<User: {}>".format(self.email)





