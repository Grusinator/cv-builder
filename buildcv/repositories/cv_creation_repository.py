import json
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User

from buildcv.models import CvCreationProcess, JobPost
from buildcv.schemas import CvContent
from cv_content.schemas import JobPosition, Education, Project, Competency
from users.models import ProfileModel
from users.schemas import Profile


class CvCreationRepository:
    profile_picture_fn = "profile_picture.jpg"


    def get_cv_creation_content(self, user: User, job_post: JobPost) -> CvContent:
        cv_creation = CvCreationProcess.objects.get(user=user, job_post=job_post)

        return CvContent(
            job_title=job_post.job_title,
            profile=Profile.model_validate(cv_creation.user.profile),
            job_positions=[JobPosition.model_validate(job) for job in cv_creation.job_positions],
            projects=[Project.model_validate(proj) for proj in cv_creation.projects],
            educations=[Education.model_validate(edu) for edu in cv_creation.educations],
            competencies=[Competency.model_validate(comp) for comp in cv_creation.competencies],
            summary=cv_creation.summary
        )

    def get_media(self, user: User):

        profile = ProfileModel.objects.get(user=user)
        picture_content = profile.profile_picture.read()
        # Assert that the profile picture content can be read and is a valid image
        image = Image.open(BytesIO(picture_content))
        image.verify()  # This will raise an exception if
        return {self.profile_picture_fn: picture_content}
