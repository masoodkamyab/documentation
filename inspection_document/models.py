from django.db import models


class InspectionDocument(models.Model):
    inspection_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
