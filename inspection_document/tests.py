from unittest.mock import patch, Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import Client
from django.test.client import encode_multipart
from rest_framework import status
from rest_framework.test import APITestCase

from inspection_document.models import InspectionDocument
from inspection_document.serializers import InspectionDocumentSerializer


class TestInspectionDocumentView(APITestCase):
    def setUp(self):
        self.inspection_url = 'https://example.com/inspection'
        self.client = Client()
        self.inspection_id = 1
        self.inspection_doc = InspectionDocument.objects.create(
            inspection_id=self.inspection_id,
            comment='Test comment'
        )
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            'id': 1,
            'name': 'Example Inspection'
        }
        with patch('requests.get', return_value=mock_response):
            self.inspection_doc_serializer = InspectionDocumentSerializer(
                instance=self.inspection_doc
            )

    def test_post_inspection_document(self):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            'id': 123, 'name': 'Example Inspection'
        }
        with patch('requests.get', return_value=mock_response):
            file = SimpleUploadedFile('test.txt', b'Test File Content')
            data = {'comment': 'Test Comment', 'file': file}
            encoded_data = encode_multipart('boundary', data)
            response = self.client.post(
                reverse(
                    'inspection-document-detail', kwargs={'inspection_id': 123}
                ),
                data=encoded_data,
                content_type='multipart/form-data; boundary=boundary'
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['inspection_id'], 123)
        self.assertIsNotNone(response.data['file'])
        self.assertEqual(
            response.data['inspection_data']['name'], 'Example Inspection'
        )

    def test_get_one_inspection_document(self):
        url = reverse(
            'inspection-document-detail', kwargs={'inspection_id': 1}
        )
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            'id': 1, 'name': 'Example Inspection'
        }
        with patch('requests.get', return_value=mock_response):
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['inspection_data']['name'], 'Example Inspection'
        )

    def test_get_all_inspection_document(self):
        url = reverse('inspection-document-list')
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            'id': 1, 'name': 'Example Inspection'
        }
        with patch('requests.get', return_value=mock_response):
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_put_inspection_document(self):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {'id': 1,
                                           'name': 'Example Inspection'}
        with patch('requests.get', return_value=mock_response):
            file = SimpleUploadedFile('test.txt', b'Test File Content 2')
            data = {'comment': 'Test Comment 2', 'file': file}
            encoded_data = encode_multipart('boundary', data)
            response = self.client.put(
                reverse(
                    'inspection-document-detail', kwargs={'inspection_id': 1}
                ),
                data=encoded_data,
                content_type='multipart/form-data; boundary=boundary',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['inspection_id'], 1)
        self.assertEqual(response.data['comment'], 'Test Comment 2')
        self.assertIsNotNone(response.data['file'])
        self.assertEqual(response.data['inspection_data']['name'],
                         'Example Inspection')