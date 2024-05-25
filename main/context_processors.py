from django.contrib.auth import get_user_model
from .models import Chief


def is_chief_user(request):
    if request.user.is_authenticated:
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        print(type(user))
        return {
            'is_chief_user': isinstance(user, Chief)
        }
    return {
        'is_chief_user': False
    }