import pytest

pytestmark = pytest.mark.dependency()


def test_get_authentication_token_using_wrong_credentials(client):
    response = client.post("/token/",
                           {"username": "superuser", "password": "wrong"})
    assert response.status_code == 401


def test_get_authentication_token(client, user_seed):
    response = client.post("/token/",
                           {"username": "superuser",
                            "password": "lookathowgoodandbigisthepass"
                            })
    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()


def test_get_and_verify_authentication_token(client, user_seed):
    auth_response = client.post("/token/",
                                {"username": "superuser",
                                 "password": "lookathowgoodandbigisthepass"
                                 })
    verification_response = client.post(
            '/token/verify/', {"token": auth_response.json()['access']})

    assert verification_response.status_code == 200


def test_get_and_refresh_authentication_token(client, user_seed):
    auth_response = client.post("/token/",
                                {"username": "superuser",
                                 "password": "lookathowgoodandbigisthepass"
                                 })

    refresh_response = client.post(
            '/token/refresh/', {"refresh": auth_response.json()['refresh']})

    assert refresh_response.status_code == 200


@pytest.mark.dependency(
    depends=[
        "test_get_authentication_token_using_wrong_credentials",
        "test_get_authentication_token",
        "test_get_and_verify_authentication_token",
        "test_get_and_refresh_authentication_token",
        ]
    )
def test_validate_authentication():
    pass
