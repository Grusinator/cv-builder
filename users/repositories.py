from .models import ProfileModel
from .schemas import Profile


class ProfileRepository:
    @staticmethod
    def get_profile(user):
        profile = ProfileModel.objects.get(user=user)
        return Profile.from_orm(profile)

    @staticmethod
    def update_profile(profile, profile_data):
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        return Profile.from_orm(profile)
