import pytest
from django.contrib.auth.models import User

@pytest.fixture
def create_user(db):
    def _make(username="demo", password="pass123", **extra):
        return User.objects.create_user(username=username, password=password, **extra)
    return _make
