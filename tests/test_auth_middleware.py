import pytest
from fastapi.testclient import TestClient
from app.main import create_app

app = create_app()
client = TestClient(app)


def test_missing_token_returns_401():
    """
    ✅ מבטיח שבקשה ללא טוקן תחזיר 401 עם הודעה ברורה.
    """
    response = client.get("/orders/1")
    assert response.status_code == 401
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid or expired token."
    assert "hint" in response.json()


def test_invalid_token_returns_401():
    """
    ✅ מבטיח שטוקן לא תקף יחזיר 401 עם אותה הודעה.
    """
    headers = {"Authorization": "Bearer this.is.not.a.valid.token"}
    response = client.get("/orders/1", headers=headers)

    assert response.status_code == 401
    body = response.json()
    assert body["error"] == "Invalid or expired token."
    assert "Please log in again" in body["hint"]


def test_forbidden_access_for_non_admin(mocker):
    """
    ✅ משתמש רגיל (לא אדמין) שמנסה לגשת לראוט של אדמין
    אמור לקבל 403 עם הודעה ברורה.
    """
    # מדמה משתמש מחובר עם role="user"
    mock_user = mocker.MagicMock()
    mock_user.role = "user"
    mock_user.id = 1

    mocker.patch("app.core.security.get_current_user", return_value=mock_user)

    response = client.get("/orders/", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 403
    assert "error" in response.json() or "You are not authorized" in response.text
