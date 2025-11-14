from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from jobs.models import Job
from profiles.models import UserProfile
from skills_extractor.extractor import extract_all
from rest_framework.permissions import IsAuthenticated,AllowAny
from .ai_reasoning import get_ai_reason,get_ai_skill_gap,generate_career_roadmap
from learning.models import LearningResource


# Create your views here.
JOB_PLATFORMS = ["LinkedIn", "BDJobs", "Glassdoor"]


class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        profile = UserProfile.objects.get(email=email)
        user_skills = [s.strip().lower() for s in (profile.skills or "").split(',')]
        user_interests = [i.strip().lower() for i in (profile.career_interests or "").split(',')]
        user_exp = profile.experience or ""

        recommended_jobs = []

        for job in Job.objects.all():
            job_skills_lower = [s.lower() for s in job.required_skills]
            overlap = list(set(user_skills) & set(job_skills_lower))

            # Skip jobs with no skill overlap
            if not overlap:
                continue

            skill_score = len(overlap) / len(job.required_skills) if job.required_skills else 0
            exp_score = 1 if job.experience_level.lower() in (user_exp.lower() or "") else 0
            interest_score = 1 if any(interest in job.title.lower() for interest in user_interests) else 0

            match_percentage = int((skill_score * 0.6 + exp_score * 0.2 + interest_score * 0.2) * 100)

            ai_reason = get_ai_reason(user_skills, user_exp, user_interests, job)

            recommended_jobs.append({
                "job_id": str(job.id),
                "title": job.title,
                "company": job.company,
                "match_percentage": match_percentage,
                "matched_skills": overlap,
                "missing_skills": list(set(job.required_skills) - set(overlap)),
                "ai_reason": ai_reason,
                "platforms": JOB_PLATFORMS
            })

        # Sort by match_percentage
        recommended_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)

        return Response({"recommended_jobs": recommended_jobs})



from dotenv import load_dotenv
load_dotenv()
import os

# AI API config
HF_API_KEY = os.getenv("api_key")
HF_API_URL = "https://router.huggingface.co/v1"

# Example job platforms
JOB_PLATFORMS = [
    {"name": "LinkedIn", "url": "https://www.linkedin.com/jobs/"},
    {"name": "Glassdoor", "url": "https://www.glassdoor.com/Job/index.htm"},
    {"name": "BDJobs", "url": "https://www.bdjobs.com/"}
]




class RecommendationsWithSkillGapView(APIView):
    """
    Returns recommended jobs with match percentage, missing skills, 
    AI-generated gap explanation, and learning resources.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        user_skills = [s.strip().lower() for s in (profile.skills or "").split(',') if s.strip()]
        user_interests = [i.strip().lower() for i in (profile.career_interests or "").split(',') if i.strip()]
        user_exp = profile.experience or ""

        recommended_jobs = []

        for job in Job.objects.all():
            job_skills_lower = [s.lower() for s in job.required_skills]
            matched_skills = list(set(user_skills) & set(job_skills_lower))
            missing_skills = list(set(job_skills_lower) - set(matched_skills))

            # Only consider jobs where at least one skill matches
            if not matched_skills:
                continue

            # Simple match score
            skill_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
            exp_score = 1 if job.experience_level.lower() in (user_exp.lower() or "") else 0
            interest_score = 1 if any(interest in job.title.lower() for interest in user_interests) else 0
            match_percentage = int((skill_score*0.6 + exp_score*0.2 + interest_score*0.2) * 100)

            # AI Skill gap explanation
            ai_reason = get_ai_skill_gap(user_skills, job.title, missing_skills) if missing_skills else "All required skills matched."

            # DB learning resources for missing skills
            recommended_resources = []
            for skill in missing_skills:
                resources = LearningResource.objects.filter(related_skills__icontains=skill)
                for res in resources:
                    recommended_resources.append({
                        "title": res.title,
                        "url": res.url,
                        "platform": res.platform,
                        "cost": res.cost,
                        "skill": skill
                    })

            recommended_jobs.append({
                "job_id": str(job.id),
                "title": job.title,
                "company": job.company,
                "match_percentage": match_percentage,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "ai_reason": ai_reason,
                "recommended_resources": recommended_resources,
                "platforms": JOB_PLATFORMS
            })

        # Sort by match_percentage descending
        recommended_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)

        return Response({"recommended_jobs": recommended_jobs})



from .serializers import TimeframeSerializer


class RoadmapGenerator(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request):

        serializer = TimeframeSerializer(data = request.data)

        if serializer.is_valid():


            profile = UserProfile.objects.get(email = request.user.email)
            print(str(profile.email))

            users_skills = profile.skills
            users_experience = profile.experience
            users_interests =  profile.career_interests
            time_frame=serializer.validated_data['time_frame']

        
            res = generate_career_roadmap(users_skills,users_interests)

            return Response(
                {   "user_skilss":users_skills,
                    "user_interests":users_interests,
                    "time_frame":time_frame,
                    "msg":res,
                }
            )


        else:
            return Response({"msg":"input data is wrong"})

