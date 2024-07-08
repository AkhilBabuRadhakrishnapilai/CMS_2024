from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            print(user)
            print(user.is_staff)
            print(password)
            print("User:", user)
            print("Stored Hashed Password:", user.password)
            print("Provided Password:", password)
            if user.check_password(password):  # Use check_password function
                print("I'm here")
                return user
            else:
                print("incorrect passwrod")
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None