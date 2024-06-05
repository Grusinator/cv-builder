from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/job-positions/", response=List[JobPositionSchema])
def get_job_positions(request):
    user = request.user
    return CvBuilderRepository.get_job_positions(user)
