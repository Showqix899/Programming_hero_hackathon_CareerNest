from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .tasks import create_user_profile

User = get_user_model()

@receiver(post_save, sender=User)
def trigger_user_profile_creation(sender, instance, created, **kwargs):
    if created:
        # Only trigger on new user registration
        create_user_profile.delay(instance.id)
