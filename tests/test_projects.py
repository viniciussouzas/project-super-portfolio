import pytest
from projects.models import Project

pytestmark = pytest.mark.dependency()


def test_project_post_request(auth_client, project_seed, profile_seed):
    response = auth_client.post(
        "/projects/",
        {
            "name": "Projeto 2",
            "description": "Descrição do projeto 2",
            "github_url": "http://myfakeurl2.com",
            "keyword": "keyword1",
            "key_skill": "key_skill1",
            "profile": profile_seed.id,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": project_seed.id + 1,
        "name": "Projeto 2",
        "description": "Descrição do projeto 2",
        "github_url": "http://myfakeurl2.com",
        "keyword": "keyword1",
        "key_skill": "key_skill1",
        "profile": profile_seed.id,
    }
    assert Project.objects.count() == 2


def test_project_get_all_request(auth_client, project_seed):
    response = auth_client.get("/projects/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [
        {
            "id": project_seed.id,
            "name": project_seed.name,
            "description": project_seed.description,
            "github_url": project_seed.github_url,
            "keyword": project_seed.keyword,
            "key_skill": project_seed.key_skill,
            "profile": project_seed.profile.id,
        }
    ]


def test_project_get_one_request(auth_client, project_seed):
    response = auth_client.get(f"/projects/{project_seed.id}/")

    assert response.status_code == 200
    assert response.json() == {
        "id": project_seed.id,
        "name": project_seed.name,
        "description": project_seed.description,
        "github_url": project_seed.github_url,
        "keyword": project_seed.keyword,
        "key_skill": project_seed.key_skill,
        "profile": project_seed.profile.id,
    }


def test_project_patch_request(auth_client, project_seed):
    response = auth_client.patch(
        f"/projects/{project_seed.id}/",
        {
            "name": "Projeto 1 alterado",
            "description": "Descrição do projeto alterada",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": project_seed.id,
        "name": "Projeto 1 alterado",
        "description": "Descrição do projeto alterada",
        "github_url": project_seed.github_url,
        "keyword": project_seed.keyword,
        "key_skill": project_seed.key_skill,
        "profile": project_seed.profile.id,
    }

    assert Project.objects.count() == 1
    assert Project.objects.get(id=project_seed.id).name == "Projeto 1 alterado"
    assert (
        Project.objects.get(id=project_seed.id).description
        == "Descrição do projeto alterada"
    )


def test_project_delete_request(auth_client, project_seed):
    response = auth_client.delete(f"/projects/{project_seed.id}/")

    assert response.status_code == 204
    assert Project.objects.count() == 0


def test_project_post_request_without_authentication(client, project_seed):
    response = client.post(
        "/projects/",
        {
            "name": "Projeto 2",
            "description": "Descrição do projeto 2",
            "github_url": "http://myfakeurl2.com",
            "keyword": "keyword1",
            "key_skill": "key_skill1",
            "profile": 1,
        },
    )

    assert response.status_code == 401
    assert Project.objects.count() == 1


def test_project_get_all_request_without_authentication(client, project_seed):
    response = client.get("/projects/")

    assert response.status_code == 401
    assert Project.objects.count() == 1


def test_project_get_one_request_without_authentication(client, project_seed):
    response = client.get(f"/projects/{project_seed.id}/")

    assert response.status_code == 401
    assert Project.objects.count() == 1


def test_project_patch_request_without_authentication(client, project_seed):
    response = client.patch(
        f"/projects/{project_seed.id}/",
        {
            "name": "Projeto 1 alterado",
            "description": "Descrição do projeto alterada",
        },
    )

    assert response.status_code == 401
    assert Project.objects.count() == 1
    assert Project.objects.get(id=project_seed.id).name == "Projeto 1"
    assert (
        Project.objects.get(id=project_seed.id).description
        == "Descrição do projeto 1"
    )


def test_project_delete_request_without_authentication(client, project_seed):
    response = client.delete(f"/projects/{project_seed.id}/")

    assert response.status_code == 401
    assert Project.objects.count() == 1


@pytest.mark.dependency(
    depends=[
        "test_project_post_request",
        "test_project_get_all_request",
        "test_project_get_one_request",
        "test_project_patch_request",
        "test_project_delete_request",
        "test_project_post_request_without_authentication",
        "test_project_get_all_request_without_authentication",
        "test_project_get_one_request_without_authentication",
        "test_project_patch_request_without_authentication",
        "test_project_delete_request_without_authentication",
    ]
)
def test_validate_projects_crud():
    pass
