"""Authentication API tests."""

import pytest


@pytest.mark.asyncio
async def test_register_and_login(client) -> None:
    """Users can register and login."""
    payload = {"email": "investor@example.com", "full_name": "Investor One", "password": "strongpass123"}
    register = await client.post("/api/v1/auth/register", json=payload)
    assert register.status_code == 201
    login = await client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert login.status_code == 200
    assert login.json()["access_token"]
