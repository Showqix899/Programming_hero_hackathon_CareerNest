from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email=models.EmailField(unique=True, null=True,blank=True)
    skills = models.JSONField(default=list,blank=True,null=True)
    experience = models.TextField(blank=True, null=True)
    career_interests = models.JSONField(default=list,blank=True,null=True)
    cv_text = models.TextField(blank=True, null=True)
    cv_pdf = models.FileField(upload_to='cv_pdfs/', blank=True, null=True)
    pdf_text=models.JSONField(default=list,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
