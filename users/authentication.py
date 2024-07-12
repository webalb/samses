from .models import CustomUser, Profile

def create_profile(backend, user, *args, **kwargs):
    """
        create profile from social authentication
    """
    Profile.objects.get_or_create(user=user)

class EmailAuthBackend:

    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username)

            if user.check_password(password): # type: ignore
                return user
            return None
        except (CustomUser.DoesNotExist, CustomUser.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None