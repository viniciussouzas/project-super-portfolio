import pytest
from projects.models import Profile
from pytest_django.asserts import assertTemplateUsed, assertContains

pytestmark = pytest.mark.dependency()


def test_profile_post_request(auth_client, profile_seed):
    response = auth_client.post(
        "/profiles/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 201
    assert Profile.objects.count() == 2
    assert Profile.objects.last().name == "Profile 2"


def test_profile_post_request_without_authentication(client, profile_seed):

    response = client.post(
        "/profiles/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 401
    assert Profile.objects.count() == 1


def test_profile_get_all_request(auth_client, profile_seed):
    response = auth_client.get("/profiles/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": profile_seed.id,
            "name": profile_seed.name,
            "github": profile_seed.github,
            "linkedin": profile_seed.linkedin,
            "bio": profile_seed.bio,
        }
    ]


def test_profile_patch_request(auth_client, profile_seed):
    response = auth_client.patch(
        f"/profiles/{profile_seed.id}/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 200
    assert Profile.objects.count() == 1
    assert Profile.objects.get().name == "Profile 2"
    assert Profile.objects.get().bio == "Bio do profile 2"


def test_profile_patch_request_without_authentication(client, profile_seed):
    response = client.patch(
        f"/profiles/{profile_seed.id}/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 401
    assert Profile.objects.count() == 1
    assert Profile.objects.get().name == profile_seed.name
    assert Profile.objects.get().bio == profile_seed.bio


def test_profile_delete_request(auth_client, profile_seed):
    response = auth_client.delete(f"/profiles/{profile_seed.id}/")
    assert response.status_code == 204
    assert Profile.objects.count() == 0


def test_profile_delete_request_without_authentication(client, profile_seed):

    response = client.delete(f"/profiles/{profile_seed.id}/")
    assert response.status_code == 401
    assert Profile.objects.count() == 1


def test_profile_template_without_authentication(client, profile_seed):

    response = client.get(f"/profiles/{profile_seed.id}/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profile_detail.html")
    assertContains(response, profile_seed.name)
    assertContains(response, profile_seed.bio)


def test_complete_profile_template_without_authentication(
    client, profile_seed, certificate_and_institution_seed
):
    response = client.get(f"/profiles/{profile_seed.id}/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profile_detail.html")
    assertContains(response, profile_seed.name)
    assertContains(response, profile_seed.bio)
    assertContains(response, profile_seed.projects.all()[0].name)
    assertContains(response, profile_seed.projects.all()[0].keyword)
    assertContains(response, profile_seed.projects.all()[0].key_skill)
    assertContains(response, profile_seed.certificates.all()[0].name)
    assertContains(
        response, profile_seed.certificates.all()[0].certifying_institution
    )


@pytest.mark.dependency(
    depends=[
        "test_profile_post_request",
        "test_profile_get_all_request",
        "test_profile_patch_request",
        "test_profile_delete_request",
    ]
)
def test_validate_profiles_crud():
    pass


@pytest.mark.dependency(
    depends=[
        "test_profile_template_without_authentication",
    ]
)
def test_validate_profiles_template():
    pass


@pytest.mark.dependency(
    depends=[
        "test_profile_template_without_authentication",
        "test_complete_profile_template_without_authentication",
    ]
)
def test_validate_complete_profiles_template():
    pass
