from ninja import Router, Schema
from typing import List
from .models import SurveyMission

api = Router()


class SurveyMissionOut(Schema):
    id: int
    name: str
    description: str
    date: str
    raster_path: str


@api.get("/", response=List[SurveyMissionOut])
def list_missions(request):
    return SurveyMission.objects.all()


@api.get("/{mission_id}", response=SurveyMissionOut)
def get_mission(request, mission_id: int):
    return SurveyMission.objects.get(id=mission_id)
