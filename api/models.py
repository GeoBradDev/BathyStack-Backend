from django.contrib.gis.db import models


class SurveyMission(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()

    track = models.LineStringField(srid=4326)  # AUV path
    footprint = models.PolygonField(srid=4326)  # Coverage area
    raster_path = models.CharField(max_length=500)  # Path to raster file

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
