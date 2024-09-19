from rest_framework.test import APIClient
from rest_framework import status

class TestCreateCollection:
    def test_if_user_is_anonymous_return_200(self):
        client = APIClient()
        response = client.post('/store/collection/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED