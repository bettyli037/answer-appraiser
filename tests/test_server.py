from fastapi.testclient import TestClient

from app.server import APP

testclient = TestClient(APP)


def test_sync_get_appraisal_400():
    """Test calling /query endpoint."""
    response = testclient.post(
        "/get_appraisal",
        json={"message": {}},
    )
    assert response.status_code == 400
