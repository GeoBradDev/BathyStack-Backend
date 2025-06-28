from ninja import Router, Schema
from typing import List
from .models import SurveyMission
from django.contrib.gis.geos import Point

api = Router()


class SurveyMissionOut(Schema):
    id: int
    name: str
    description: str
    date: str
    raster_path: str

class PointQuery(Schema):
    lat: float
    lng: float


@api.get("/", response=List[SurveyMissionOut])
def list_missions(request):
    return SurveyMission.objects.all()


@api.get("/{mission_id}", response=SurveyMissionOut)
def get_mission(request, mission_id: int):
    return SurveyMission.objects.get(id=mission_id)

@api.get("/covering-point", response=List[SurveyMissionOut])
def missions_covering_point(request, q: PointQuery):
    point = Point(q.lng, q.lat, srid=4326)
    return SurveyMission.objects.filter(footprint__intersects=point)
