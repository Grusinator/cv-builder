import json

from django.contrib.auth.models import User

from buildcv.models import CvCreationProcess, JobPost
from buildcv.schemas import CvContent
from cv_content.schemas import JobPosition, Education, Project, Competency
from users.schemas import Profile


class CvCreationRepository:

    def get_cv_creation_content(self, user: User, job_post: JobPost) -> CvContent:
        cv_creation = CvCreationProcess.objects.get(user=user, job_post=job_post)

        return CvContent(
            job_title=job_post.job_title,
            profile=Profile.from_orm(cv_creation.user.profile),
            job_positions=[JobPosition(**job) for job in cv_creation.job_positions],
            projects=[Project(**proj) for proj in cv_creation.projects],
            educations=[Education(**edu) for edu in cv_creation.educations],
            competencies=[Competency(**comp) for comp in cv_creation.competencies],
            summary=cv_creation.summary
        )
