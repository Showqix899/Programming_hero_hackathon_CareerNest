import uuid
from django.db import models

class Job(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('Fresher', 'Fresher'),
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
    ]

    JOB_TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('Part-time', 'Part-time'),
        ('Full-time', 'Full-time'),
        ('Freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100, default="Remote")
    required_skills = models.JSONField(default=list)  # e.g., ["Python", "Django"]
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
