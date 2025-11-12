from celery import shared_task
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@shared_task
def create_user_profile(user_id):
    try:
        user = User.objects.get(id=user_id)
        # Create profile only if it does not exist
        if not hasattr(user, 'profile'):
            UserProfile.objects.create(user=user)
            print(f"UserProfile created for {user.email}")
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
