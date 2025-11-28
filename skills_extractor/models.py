from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class UserSkills(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='skills')
    #list field
    skills = models.JSONField(default=dict)  # e.g., {"skills_found": [], "tools_found": [], "roles_found": []}
    tools = models.JSONField(default=dict)
    roles = models.JSONField(default=dict)
    
    
    def __str__(self):
        return f"Skills for {self.user.email}"