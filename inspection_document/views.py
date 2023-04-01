import os

import requests
from rest_framework import generics
from rest_framework.response import Response
from .models import InspectionDocument
from .serializers import InspectionDocumentSerializer


class InspectionDocumentView(
    generics.ListCreateAPIView, generics.RetrieveUpdateAPIView
):
    queryset = InspectionDocument.objects.all()
    serializer_class = InspectionDocumentSerializer
    lookup_field = 'inspection_id'

    def get(self, request, *args, **kwargs):
        if 'inspection_id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        inspection_id = self.kwargs['inspection_id']
        try:
            inspection_doc = InspectionDocument.objects.get(
                inspection_id=inspection_id
            )
        except InspectionDocument.DoesNotExist:
            return Response(
                {'error': 'Inspection document does not exist.'}, status=404
            )

        comment = request.data.get('comment', inspection_doc.comment)
        file = request.data.get('file')
        if file:
            inspection_doc.file = request.FILES.get('file')

        inspection_doc.comment = comment
        inspection_doc.file = file if file else inspection_doc.file
        inspection_doc.save()

        serializer = self.get_serializer(
            inspection_doc,
            context={'request': request, 'inspection_id': inspection_id},
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        inspection_id = self.kwargs['inspection_id']

        try:
            inspection_doc = InspectionDocument.objects.get(
                inspection_id=inspection_id
            )
            serializer = self.get_serializer(inspection_doc)
            return Response(serializer.data, status=200)
        except InspectionDocument.DoesNotExist:
            pass

        inspection_url = os.environ.get('INSPECTION_URL')
        if not inspection_url:
            return Response(
                {'error': 'Missing INSPECTION_URL environment variable'},
                status=500
            )
        inspection_url = f'{inspection_url}/{inspection_id}'

        response = requests.get(inspection_url)
        if response.status_code != 200:
            return Response({'error': 'Inspection not found'}, status=404)

        request.data['inspection_id'] = inspection_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inspection_doc = serializer.save(inspection_id=inspection_id)
        serializer = self.get_serializer(
            inspection_doc,
            context={'request': request, 'inspection_id': inspection_id}
        )
        return Response(serializer.data, status=201)
