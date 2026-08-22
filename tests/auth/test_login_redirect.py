"""Regression tests for the login ``next`` redirect whitelist.

The redirect target must be provably server-controlled (CodeQL rule
``py/url-redirection``): only exact relative-path matches from the
whitelist are honoured, everything else falls back to a server-generated
URL.
"""

import pytest

from app.database import db
from app.database.models import User


@pytest.fixture
def user(db, client):
    """Create an active user for login attempts.

    The client session is logged out first: flask-login keeps the user id
    in the session cookie, so without an explicit logout the *next*
    parametrized case hits the already-authenticated early return and
    # redirect assertions see the fallback instead of ``next``.
    """
    import uuid

    from flask import g

    # The session-scoped ``db`` fixture keeps ONE app context pushed for the
    # whole run; Flask reuses it for same-app requests, and flask-login caches
    # ``_login_user`` on ``g`` — so a login in an earlier test would make
    # ``current_user`` authenticated here. Reset it.
    if hasattr(g, "_login_user"):
        del g._login_user

    username = f"redirect_user_{uuid.uuid4().hex[:8]}"
    user = User(username=username, email=f"{username}@example.com")
    user.password = "correct-password"
    db.session.add(user)
    db.session.commit()
    yield user

    if hasattr(g, "_login_user"):
        del g._login_user


def _login(client, next_value=None, username="redirect_user"):
    """POST valid credentials, optionally with a ``next`` param."""
    url = "/auth/login"
    if next_value is not None:
        url += f"?next={next_value}"
    return client.post(
        url,
        data={"username": username, "password": "correct-password"},
        follow_redirects=False,
    )


@pytest.mark.parametrize(
    "next_value,expected_location",
    [
        # Exact whitelist matches redirect to the exact whitelisted path
        ("/items/all_events", "/items/all_events"),
        ("/profile", "/profile"),
        ("/dashboard", "/dashboard"),
        # Absolute URLs, schemes and off-whitelist paths fall back to the
        # server-generated default (url_for("items.all_events") == "/items/")
        ("https://evil.example.com", "/items/"),
        ("//evil.example.com", "/items/"),
        ("http://evil.example.com", "/items/"),
        ("/items/all_events/extra", "/items/"),
        ("/not-in-whitelist", "/items/"),
    ],
)
def test_login_next_redirect_whitelist(client, user, next_value, expected_location):
    """Only whitelisted relative paths are honoured as redirect targets."""
    response = _login(client, next_value, username=user.username)

    assert response.status_code == 302
    assert response.location == expected_location


def test_login_without_next_falls_back_to_default(client, user):
    """No ``next`` param redirects to the default page."""
    response = _login(client, username=user.username)

    assert response.status_code == 302
    assert response.location == "/items/"
