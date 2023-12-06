import pytest
from projects.models import CertifyingInstitution, Certificate
from rest_framework.test import APIClient

pytestmark = pytest.mark.dependency()


def test_certificate_post_request(
    auth_client: APIClient, certificate_and_institution_seed, profile_seed
):
    certificate, certifying_institution = certificate_and_institution_seed
    response = auth_client.post(
        "/certificates/",
        {
            "name": "Certificate 2",
            "certifying_institution": certifying_institution.id,
            "profiles": [profile_seed.id],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json().keys() == {
        "id",
        "name",
        "certifying_institution",
        "timestamp",
        "profiles",
    }
    assert response.json()["id"] == certificate.id + 1
    assert response.json()["name"] == "Certificate 2"
    assert (
        response.json()["certifying_institution"] == certifying_institution.id
    )
    assert Certificate.objects.count() == 2


def test_certificate_post_request_without_authentication(
    client, certificate_and_institution_seed
):
    response = client.post(
        "/certificates/",
        {
            "name": "Certificate 2",
            "certifying_institution": 1,
            "profiles": [1],
        },
        format="json",
    )
    assert response.status_code == 401
    assert Certificate.objects.count() == 1


def test_certificate_get_all_request(
    auth_client, certificate_and_institution_seed
):
    response = auth_client.get("/certificates/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].keys() == {
        "id",
        "name",
        "certifying_institution",
        "timestamp",
        "profiles",
    }

    certificate, _ = certificate_and_institution_seed
    assert response.json()[0]["id"] == certificate.id
    assert response.json()[0]["name"] == certificate.name
    assert (
        response.json()[0]["certifying_institution"]
        == certificate.certifying_institution.id
    )


def test_certificate_get_all_request_without_authentication(client):
    response = client.get("/certificates/")
    assert response.status_code == 401


def test_certificate_get_one_request(
    auth_client, certificate_and_institution_seed
):
    certificate, _ = certificate_and_institution_seed
    response = auth_client.get(f"/certificates/{certificate.id}/")

    assert response.status_code == 200
    assert response.json().keys() == {
        "id",
        "name",
        "certifying_institution",
        "timestamp",
        "profiles",
    }
    assert response.json()["id"] == certificate.id
    assert response.json()["name"] == certificate.name
    assert (
        response.json()["certifying_institution"]
        == certificate.certifying_institution.id
    )


def test_certificate_get_one_request_without_authentication(client):
    response = client.get("/certificates/1/")
    assert response.status_code == 401


def test_certificate_patch_request(
    auth_client, certificate_and_institution_seed
):
    certificate, _ = certificate_and_institution_seed
    response = auth_client.patch(
        f"/certificates/{certificate.id}/",
        {
            "name": "Certificate 2",
        },
        format="json",
    )

    assert response.status_code == 200
    assert Certificate.objects.count() == 1
    assert Certificate.objects.get().name == "Certificate 2"


def test_certificate_patch_request_without_authentication(
    client, certificate_and_institution_seed
):
    response = client.patch(
        "/certificates/1/",
        {
            "name": "Certificate 2",
        },
        format="json",
    )
    assert response.status_code == 401
    assert Certificate.objects.count() == 1
    assert Certificate.objects.get().name == "Certificate 1"


def test_certificate_delete_request(
    auth_client, certificate_and_institution_seed
):
    certificate, _ = certificate_and_institution_seed
    response = auth_client.delete(f"/certificates/{certificate.id}/")
    assert response.status_code == 204
    assert Certificate.objects.count() == 0


def test_certificate_delete_request_without_authentication(
    client, certificate_and_institution_seed
):
    certificate, _ = certificate_and_institution_seed
    response = client.delete(f"/certificates/{certificate.id}/")
    assert response.status_code == 401
    assert Certificate.objects.count() == 1


def test_certifying_institution_post_request(
    auth_client, certificate_and_institution_seed
):
    response = auth_client.post(
        "/certifying-institutions/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
            "certificates": [{"name": "Certificate 2"}],
        },
        format="json",
    )

    assert response.status_code == 201

    _, certifying_institution = certificate_and_institution_seed
    response_json = response.json()
    assert response.json().keys() == {"id", "name", "url", "certificates"}

    assert response_json["id"] == certifying_institution.id + 1
    assert response_json["name"] == "Certifying Institution 2"
    assert response_json["url"] == "http://myfakeurl.com"
    assert response_json["certificates"][0]["name"] == "Certificate 2"
    assert CertifyingInstitution.objects.count() == 2
    assert Certificate.objects.count() == 2


def test_certifying_institution_get_all_request(
    auth_client, certificate_and_institution_seed
):
    _, certifying_institution = certificate_and_institution_seed
    response = auth_client.get("/certifying-institutions/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].keys() == {"id", "name", "url", "certificates"}
    assert response.json()[0]["id"] == certifying_institution.id
    assert response.json()[0]["name"] == certifying_institution.name
    assert response.json()[0]["url"] == certifying_institution.url
    assert (
        response.json()[0]["certificates"][0]["name"]
        == certifying_institution.certificates.all()[0].name
    )


def test_certifying_institution_get_one_request(
    auth_client, certificate_and_institution_seed
):
    _, certifying_institution = certificate_and_institution_seed
    response = auth_client.get(
        f"/certifying-institutions/{certifying_institution.id}/"
    )

    assert response.status_code == 200
    assert response.json().keys() == {"id", "name", "url", "certificates"}
    assert response.json()["id"] == certifying_institution.id
    assert response.json()["name"] == certifying_institution.name
    assert response.json()["url"] == certifying_institution.url
    assert (
        response.json()["certificates"][0]["name"]
        == certifying_institution.certificates.all()[0].name
    )


def test_certifying_institution_patch_request(
    auth_client, certificate_and_institution_seed
):
    _, certifying_institution = certificate_and_institution_seed
    response = auth_client.patch(
        f"/certifying-institutions/{certifying_institution.id}/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.json().keys() == {"id", "name", "url", "certificates"}
    assert response.json()["id"] == certifying_institution.id
    assert response.json()["name"] == "Certifying Institution 2"
    assert response.json()["url"] == "http://myfakeurl.com"
    assert CertifyingInstitution.objects.count() == 1
    assert Certificate.objects.count() == 1


def test_certifying_institution_delete_request(
    auth_client, certificate_and_institution_seed
):
    _, certifying_institution = certificate_and_institution_seed
    response = auth_client.delete(
        f"/certifying-institutions/{certifying_institution.id}/"
    )
    assert response.status_code == 204
    assert CertifyingInstitution.objects.count() == 0
    assert Certificate.objects.count() == 0


def test_certifying_institution_post_request_without_authentication(
    client, certificate_and_institution_seed
):

    response = client.post(
        "/certifying-institutions/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
            "certificates": [{"name": "Certificate 2"}],
        },
        format="json",
    )

    assert response.status_code == 401
    assert CertifyingInstitution.objects.count() == 1
    assert Certificate.objects.count() == 1


def test_certifying_institution_get_all_request_without_authentication(client):
    response = client.get("/certifying-institutions/")
    assert response.status_code == 401


def test_certifying_institution_get_one_request_without_authentication(client):
    response = client.get("/certifying-institutions/1/")
    assert response.status_code == 401


def test_certifying_institution_patch_request_without_authentication(
    client, certificate_and_institution_seed
):

    response = client.patch(
        "/certifying-institutions/1/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
        },
        format="json",
    )
    assert response.status_code == 401
    assert CertifyingInstitution.objects.count() == 1
    assert (
        CertifyingInstitution.objects.get().name == "Certifying Institution 1"
    )
    assert Certificate.objects.count() == 1


def test_certifying_institution_delete_request_without_authentication(
    client, certificate_and_institution_seed
):
    response = client.delete("/certifying-institutions/1/")
    assert response.status_code == 401
    assert CertifyingInstitution.objects.count() == 1
    assert Certificate.objects.count() == 1


@pytest.mark.dependency(
    depends=[
        "test_certificate_post_request",
        "test_certificate_get_all_request",
        "test_certificate_get_one_request",
        "test_certificate_patch_request",
        "test_certificate_delete_request",
        "test_certificate_post_request_without_authentication",
        "test_certificate_get_all_request_without_authentication",
        "test_certificate_get_one_request_without_authentication",
        "test_certificate_patch_request_without_authentication",
        "test_certificate_delete_request_without_authentication",
        "test_certifying_institution_post_request",
        "test_certifying_institution_get_all_request",
        "test_certifying_institution_get_one_request",
        "test_certifying_institution_patch_request",
        "test_certifying_institution_delete_request",
    ]
)
def test_validate_certificate_and_certifying_institutions_crud():
    pass
