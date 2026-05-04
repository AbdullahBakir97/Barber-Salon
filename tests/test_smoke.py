"""Smoke tests — minimum viable signal that the project boots in CI."""
import pytest


@pytest.mark.django_db
def test_django_settings_load():
    """Django settings module imports cleanly."""
    from django.conf import settings
    assert settings.DATABASES, "settings.DATABASES is empty"


def test_apps_registry():
    """The app registry initializes without error."""
    import django
    django.setup()
    from django.apps import apps
    assert apps.ready or apps.populate(["django.contrib.contenttypes"])


def test_truth():
    assert True, "sanity check — should always pass"
