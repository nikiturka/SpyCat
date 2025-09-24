from decimal import Decimal
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .models import SpyCat


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mock_catapi(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            status_code = 200
            def json(self):
                return [{"name": "Siamese"}, {"name": "Persian"}]
        return FakeResponse()
    monkeypatch.setattr("requests.get", fake_get)


@pytest.mark.django_db
class TestSpyCatAPI:
    def test_create_spycat_valid_breed(self, api_client, mock_catapi):
        response = api_client.post(reverse("list-spy-cats"), {
            "name": "Felix",
            "years_of_experience": 3,
            "breed": "Siamese",
            "salary": "1000.00"
        }, format="json")
        assert response.status_code == 201

    def test_create_spycat_invalid_breed(self, api_client, mock_catapi):
        response = api_client.post(reverse("list-spy-cats"), {
            "name": "Tom",
            "years_of_experience": 2,
            "breed": "UnknownBreed",
            "salary": "1000.00"
        }, format="json")
        assert response.status_code == 400

    def test_create_cat_negative_salary(self, api_client, mock_catapi):
        response = api_client.post(reverse("list-spy-cats"), {
            "name": "Garfield",
            "years_of_experience": 5,
            "breed": "Siamese",
            "salary": -1000
        }, format="json")
        assert response.status_code == 400

    def test_create_cat_negative_years_of_experience(self, api_client, mock_catapi):
        response = api_client.post(reverse("list-spy-cats"), {
            "name": "Tom",
            "years_of_experience": -2,
            "breed": "Siamese",
            "salary": 1000
        }, format="json")
        assert response.status_code == 400

    def test_create_cat_non_integer_years_of_experience(self, api_client, mock_catapi):
        response = api_client.post(reverse("list-spy-cats"), {
            "name": "Jerry",
            "years_of_experience": "abc",
            "breed": "Siamese",
            "salary": 1000
        }, format="json")
        assert response.status_code == 400

    def test_update_cat_salary_negative(self, api_client):
        cat = SpyCat.objects.create(name="Felix", years_of_experience=3, breed="Siamese", salary=1000)
        url = reverse("spy-cat-detail", args=[cat.id])

        response = api_client.patch(url, {"salary": -500}, format="json")

        assert response.status_code == 400

    def test_update_cat_salary(self, api_client):
        cat = SpyCat.objects.create(name="Felix", years_of_experience=3, breed="Siamese", salary=1000)
        url = reverse("spy-cat-detail", args=[cat.id])

        api_client.patch(url, {"salary": 2000}, format="json")
        cat.refresh_from_db()

        assert cat.salary == Decimal("2000")

    def test_delete_cat(self, api_client):
        cat = SpyCat.objects.create(name="Felix", years_of_experience=3, breed="Siamese", salary=1000)
        url = reverse("spy-cat-detail", args=[cat.id])

        response = api_client.delete(url)

        assert response.status_code == 204
