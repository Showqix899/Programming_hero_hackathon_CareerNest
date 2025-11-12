from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Seed database with job data'

    def handle(self, *args, **kwargs):
        jobs_data = [
            {
                "title": "Frontend Developer Intern",
                "company": "TechNova",
                "location": "Remote",
                "required_skills": ["HTML", "CSS", "JavaScript", "React"],
                "experience_level": "Fresher",
                "job_type": "Internship",
            },
            {
                "title": "Backend Developer",
                "company": "DataWave",
                "location": "Dhaka",
                "required_skills": ["Python", "Django", "REST API"],
                "experience_level": "Junior",
                "job_type": "Full-time",
            },
            {
                "title": "Data Analyst Intern",
                "company": "InsightIQ",
                "location": "Remote",
                "required_skills": ["Python", "Excel", "Pandas", "SQL"],
                "experience_level": "Fresher",
                "job_type": "Internship",
            },
            {
                "title": "Graphic Designer",
                "company": "PixelCraft",
                "location": "Chittagong",
                "required_skills": ["Photoshop", "Illustrator", "Figma"],
                "experience_level": "Junior",
                "job_type": "Part-time",
            },
            {
                "title": "Marketing Intern",
                "company": "BrandMinds",
                "location": "Remote",
                "required_skills": ["Communication", "SEO", "Social Media"],
                "experience_level": "Fresher",
                "job_type": "Internship",
            },
            {
                "title": "UI/UX Designer",
                "company": "DesignFlow",
                "location": "Dhaka",
                "required_skills": ["Figma", "UX Research", "Wireframing"],
                "experience_level": "Junior",
                "job_type": "Full-time",
            },
            {
                "title": "Software Engineer Trainee",
                "company": "SoftCom",
                "location": "Remote",
                "required_skills": ["Python", "Git", "Teamwork"],
                "experience_level": "Fresher",
                "job_type": "Internship",
            },
            {
                "title": "Mobile App Developer",
                "company": "Appify",
                "location": "Dhaka",
                "required_skills": ["Flutter", "Firebase"],
                "experience_level": "Junior",
                "job_type": "Full-time",
            },
            {
                "title": "Content Writer",
                "company": "WordFlow",
                "location": "Remote",
                "required_skills": ["Writing", "SEO", "Creativity"],
                "experience_level": "Fresher",
                "job_type": "Freelance",
            },
            {
                "title": "AI Research Intern",
                "company": "DeepVision",
                "location": "Remote",
                "required_skills": ["Python", "TensorFlow", "ML"],
                "experience_level": "Fresher",
                "job_type": "Internship",
            },
        ]

        for job_data in jobs_data:
            Job.objects.get_or_create(**job_data)

        self.stdout.write(self.style.SUCCESS('✅  Jobs seeded successfully!'))
