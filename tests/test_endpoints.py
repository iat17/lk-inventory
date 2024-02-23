import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_healthcheck(client):
    response = await client.get('/v1/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}


@pytest.mark.asyncio
async def test_create_user(client):
    client_json = {"user_id": "abc",
                   'phone': '+71234567890',
                   'email': 'test@m.com',
                   'name': 'test_name',
                   'last_name': 'test_last_name',
                   "password": "123"}
    response = await client.post("/api/v1/users", json=client_json)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_accounts(client, create_fake_accounts, override_auth_check_dependency):
    query_params = {"offset": 1, "limit": 5}
    response = await client.get("/api/v1/accounts", params=query_params)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['entries']) == 5
    assert response.json()['totalCount'] == 9


@pytest.mark.asyncio
async def test_get_account(client, create_fake_accounts, override_auth_check_dependency):
    response = await client.get("/api/v1/accounts/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == 1


@pytest.mark.asyncio
async def test_get_services_by_account(client,
                                       create_fake_service_account_links,
                                       override_auth_check_dependency):
    query_params = {"offset": 0, "limit": 4}
    response = await client.get("/api/v1/accounts/1/services", params=query_params)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['entries']) == 1
    assert response.json()['totalCount'] == 1


@pytest.mark.asyncio
async def test_bind_service_to_account(client, create_fake_service_account_links, override_auth_check_dependency):
    response = await client.post("/api/v1/accounts/5/service/1", json={'plan_id': 3})
    assert response.status_code == status.HTTP_200_OK
