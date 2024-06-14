import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from buildcv.repositories.cv_creation_repository import CvCreationRepository
from buildcv.schemas import CvContent
from buildcv.services.build_latex_cv_service import BuildLatexCVService
from users.models import ProfileModel
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

class TestLatexContentBuilder:

    def test_render_template(self, cv_content: CvContent, file_regression):
        latex_builder = BuildLatexCVService()
        output_tex_file = "latex_workspace/test.tex"
        latex_builder.render_template(cv_content, output_tex_file)
        file_regression.check(open(output_tex_file).read(), extension=".tex")

    def test_build_content(self, cv_content: CvContent):
        latex_builder = BuildLatexCVService()
        latex_builder.compile_latex_to_pdf = lambda x: "latex_workspace/cv.pdf"
        latex_builder.build_cv_from_content(cv_content)
        assert os.path.exists("latex_workspace/cv.pdf")

    @pytest.mark.django_db
    def test_build_content_with_media(self, cv_content: CvContent, profile_in_db: ProfileModel):
        latex_builder = BuildLatexCVService()
        repository = CvCreationRepository()
        media = repository.get_media(user=profile_in_db.user)
        with TemporaryDirectory() as temp_dir:
            latex_builder.save_media(media, temp_dir)
        assert os.path.exists(Path(temp_dir) / repository.profile_picture_fn)


    @pytest.mark.django_db
    def test_read_media(self, profile_in_db):
        # Load an image file from a custom path
        with open("media/profile_pictures/IMG_2411.jpg", "rb") as image_file:
            profile_in_db.profile_picture.save(
                "test_image.jpg",
                SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg"),
                save=True
            )

        # Retrieve the profile picture content
        profile_picture_content = profile_in_db.profile_picture.read()

        # Assert that the profile picture content can be read and is a valid image
        image = Image.open(BytesIO(profile_picture_content))
        image.verify()  # This will raise an exception if the image is not valid

        assert profile_in_db.profile_picture.name == "test_image.jpg"
        assert len(profile_picture_content) > 0

