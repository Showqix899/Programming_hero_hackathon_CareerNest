from django.core.management.base import BaseCommand
from learning.models import LearningResource
import random

class Command(BaseCommand):
    help = "Seed the LearningResource table with sample data"

    def handle(self, *args, **kwargs):
        resources = [
            {
                "title": "HTML for Beginners",
                "platform": "YouTube",
                "url": "https://www.youtube.com/watch?v=qz0aGYrrlhU",
                "related_skills": ["HTML", "Web Development"],
                "cost": "Free"
            },
            {
                "title": "Python Crash Course",
                "platform": "Coursera",
                "url": "https://coursera.org/python-crash-course",
                "related_skills": ["Python", "Programming"],
                "cost": "Free"
            },
            {
                "title": "Excel Essentials",
                "platform": "Udemy",
                "url": "https://udemy.com/excel-essentials",
                "related_skills": ["Excel", "Data Analysis"],
                "cost": "Paid"
            },
            {
                "title": "Effective Communication",
                "platform": "Skillshare",
                "url": "https://skillshare.com/effective-communication",
                "related_skills": ["Communication", "Soft Skills"],
                "cost": "Paid"
            },
            {
                "title": "JavaScript Basics",
                "platform": "YouTube",
                "url": "https://youtube.com/js-basics",
                "related_skills": ["JavaScript", "Frontend"],
                "cost": "Free"
            },
            {
                "title": "Intro to Machine Learning",
                "platform": "Coursera",
                "url": "https://coursera.org/ml-intro",
                "related_skills": ["Machine Learning", "Python"],
                "cost": "Free"
            },
            {
                "title": "Creative Design Basics",
                "platform": "Canva Design School",
                "url": "https://designschool.canva.com/",
                "related_skills": ["Design", "Creativity"],
                "cost": "Free"
            },
            {
                "title": "Django for Beginners",
                "platform": "Udemy",
                "url": "https://udemy.com/django-for-beginners",
                "related_skills": ["Python", "Django", "Backend"],
                "cost": "Paid"
            },
            {
                "title": "Data Visualization with Excel",
                "platform": "LinkedIn Learning",
                "url": "https://linkedin.com/learning/excel-visualization",
                "related_skills": ["Excel", "Data Visualization"],
                "cost": "Paid"
            },
            {
                "title": "Responsive Web Design",
                "platform": "freeCodeCamp",
                "url": "https://freecodecamp.org/learn/responsive-web-design",
                "related_skills": ["HTML", "CSS", "Web Design"],
                "cost": "Free"
            },
            # add up to 15–20 total entries
        ]

        for data in resources:
            LearningResource.objects.get_or_create(**data)

        self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(resources)} learning resources successfully!"))
