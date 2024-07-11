from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

users = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request,email=None,password=None,**kwargs):
        try:
            print(email,password)
            user = users.objects.get(email=email)
            print(user)
            if user.check_password(password):
                return user
        except users.DoesNotExist:
            return None
        
    def get_user(self,user_id):
        try:
            return users.objects.get(pk=user_id)
        except users.DoesNotExist:
            return None