import os

import requests
from rest_framework import serializers

from inspection_document.models import InspectionDocument


class InspectionDocumentSerializer(serializers.ModelSerializer):
    inspection_data = serializers.SerializerMethodField()

    def get_inspection_data(self, obj):
        inspection_id = obj.inspection_id
        inspection_url = os.environ.get('INSPECTION_URL')
        inspection_url = f'{inspection_url}/{inspection_id}'
        response = requests.get(inspection_url)
        inspection_data = response.json()
        return inspection_data

    def create(self, validated_data):
        inspection_id = validated_data.pop('inspection_id')
        inspection_doc = InspectionDocument.objects.create(
            inspection_id=inspection_id, **validated_data
        )
        return inspection_doc

    class Meta:
        model = InspectionDocument
        fields = ('inspection_id', 'comment', 'file', 'inspection_data')
