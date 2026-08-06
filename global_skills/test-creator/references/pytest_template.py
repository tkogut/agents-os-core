import pytest
from httpx import AsyncClient, ASGITransport
from main import app, get_db, get_current_user
from models import User

# Szablon testu integracyjnego API FastAPI w pytest

async def override_current_user():
    return User(id=1, username="testadmin", role="admin")

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def setup_test_environment():
    # Nadpisanie zależności autoryzacji
    app.dependency_overrides[get_current_user] = override_current_user
    yield
    app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_endpoint_logic(setup_test_environment):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/analytics/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "yield_total_7d" in data
