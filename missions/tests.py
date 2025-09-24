import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from spy_cats.models import SpyCat
from .models import Mission, Target


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def spy_cat():
    return SpyCat.objects.create(name="Felix", years_of_experience=3, breed="Siamese", salary=1000)


@pytest.fixture
def mission_factory():
    def create_mission(cat=None, completed=False):
        return Mission.objects.create(cat=cat, completed=completed)
    return create_mission


@pytest.fixture
def target_factory():
    def create_target(mission, name="Target", country="US", notes="", completed=False):
        return Target.objects.create(mission=mission, name=name, country=country, notes=notes, completed=completed)
    return create_target


@pytest.mark.django_db
class TestMissionAPI:
    def test_create_mission_with_valid_targets(self, api_client):
        data = {
            "completed": False,
            "targets": [
                {"name": "Target1", "country": "US", "notes": "", "completed": False},
                {"name": "Target2", "country": "FR", "notes": "", "completed": False}
            ]
        }
        response = api_client.post(reverse("mission-list"), data, format="json")
        assert response.status_code == 201

    def test_create_mission_with_zero_targets(self, api_client):
        response = api_client.post(reverse("mission-list"), {"completed": False, "targets": []}, format="json")
        assert response.status_code == 400

    def test_create_mission_with_more_than_three_targets(self, api_client):
        targets = [{"name": f"T{i}", "country": "US", "notes": "", "completed": False} for i in range(4)]
        response = api_client.post(reverse("mission-list"), {"completed": False, "targets": targets}, format="json")
        assert response.status_code == 400

    def test_assign_cat_to_several_missions(self, api_client, spy_cat, mission_factory):
        mission1 = mission_factory()
        mission2 = mission_factory()

        url1 = reverse("mission-detail", args=[mission1.id])
        api_client.patch(url1, {"cat": spy_cat.id}, format="json")

        url2 = reverse("mission-detail", args=[mission2.id])
        response = api_client.patch(url2, {"cat": spy_cat.id}, format="json")
        assert response.status_code == 400

    def test_update_target_notes_and_completed(self, api_client, mission_factory, target_factory):
        mission = mission_factory()
        target = target_factory(mission, name="Target1")

        url = reverse("target-detail", args=[target.id])

        response1 = api_client.patch(url, {"notes": "New notes"}, format="json")

        response2 = api_client.patch(url, {"completed": True}, format="json")

        assert response1.status_code == response2.status_code == 200

    def test_cannot_edit_notes_if_mission_completed(self, api_client, mission_factory, target_factory):
        mission = mission_factory(completed=True)
        target = target_factory(mission, notes="Old notes")

        url = reverse("target-detail", args=[target.id])
        response = api_client.patch(url, {"notes": "New notes"}, format="json")

        assert response.status_code == 400

    def test_cannot_edit_notes_if_target_completed(self, api_client, mission_factory, target_factory):
        mission = mission_factory(completed=False)
        target = target_factory(mission, notes="Old notes", completed=True)

        url = reverse("target-detail", args=[target.id])
        response = api_client.patch(url, {"notes": "New notes"}, format="json")

        assert response.status_code == 400

    def test_delete_mission_without_cat(self, api_client, mission_factory):
        mission = mission_factory()
        url = reverse("mission-detail", args=[mission.id])
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_delete_mission_with_cat(self, api_client, mission_factory, spy_cat):
        mission = mission_factory(cat=spy_cat)
        url = reverse("mission-detail", args=[mission.id])
        response = api_client.delete(url)
        assert response.status_code == 400
