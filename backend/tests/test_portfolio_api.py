"""Portfolio API tests."""

import pytest


@pytest.mark.asyncio
async def test_portfolio_crud_flow(client) -> None:
    """Authenticated users can create portfolios and holdings."""
    user = {"email": "p@example.com", "full_name": "Portfolio User", "password": "strongpass123"}
    await client.post("/api/v1/auth/register", json=user)
    login = await client.post("/api/v1/auth/login", json={"email": user["email"], "password": user["password"]})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    created = await client.post("/api/v1/portfolio", json={"name": "Long Term"}, headers=headers)
    assert created.status_code == 201
    portfolio_id = created.json()["id"]

    holding = await client.post(
        f"/api/v1/portfolio/{portfolio_id}/holding",
        json={"ticker": "TCS", "quantity": "2", "average_price": "3500"},
        headers=headers,
    )
    assert holding.status_code == 201
    fetched = await client.get(f"/api/v1/portfolio/{portfolio_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["holdings"][0]["ticker"] == "TCS"
