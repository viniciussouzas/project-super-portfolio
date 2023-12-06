import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
try:
    from projects import models
except ImportError:
    models = None


@pytest.fixture()
def user_seed():
    return User.objects.create_user(
        username="superuser",
        password="lookathowgoodandbigisthepass",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture()
def profile_seed():
    return models.Profile.objects.create(
        name="Profile 1",
        github="http://myfakeurl.com",
        linkedin="http://myfakeurl.com",
        bio="Bio do profile 1",
    )


@pytest.fixture()
def project_seed(profile_seed):
    return models.Project.objects.create(
        name="Projeto 1",
        description="Descrição do projeto 1",
        github_url="http://myfakeurl.com",
        keyword="keyword1",
        key_skill="key_skill1",
        profile=profile_seed,
    )


@pytest.fixture()
def certificate_and_institution_seed(project_seed, profile_seed):
    cert_institution = models.CertifyingInstitution.objects.create(
        name="Certifying Institution 1",
        url="http://myfakeurl.com",
    )

    certificate = models.Certificate.objects.create(
        name="Certificate 1",
        certifying_institution=cert_institution,
    )

    profile_seed.certificates.add(certificate)
    return certificate, cert_institution


@pytest.fixture(autouse=True)
def allow_database(db):
    ...


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture()
def auth_client(client: APIClient, user_seed):
    res = client.post(
        "/token/",
        data={
            "username": user_seed.username,
            "password": "lookathowgoodandbigisthepass",
        },
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.json()['access']}")
    return client
