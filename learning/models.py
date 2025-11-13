import uuid
from django.db import models

class LearningResource(models.Model):
    RESOURCE_TYPE = [
        ('Free', 'Free'),
        ('Paid', 'Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    platform = models.CharField(max_length=100)
    url = models.URLField()
    related_skills = models.JSONField()  # store as list, e.g. ["Python", "HTML"]
    cost = models.CharField(max_length=10, choices=RESOURCE_TYPE)

    def __str__(self):
        return self.title
