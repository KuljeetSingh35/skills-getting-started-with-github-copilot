from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_root_redirects_to_static():
    r = client.get("/", allow_redirects=False)
    assert r.status_code in (301, 302, 307, 308)
    assert r.headers.get("location") == "/static/index.html"


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "tester+pytest@example.com"

    # Ensure signup succeeds
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Signing up again should fail
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 400

    # Unregister should succeed
    r = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert r.status_code == 200

    # Unregistering again should fail
    r = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert r.status_code == 400
