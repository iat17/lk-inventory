import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_healthcheck(client):
    response = await client.get('/v1/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
