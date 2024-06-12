#!/usr/bin/env python3
"""
Module for testing the web server endpoints
"""

import requests

BASE_URL = "http://0.0.0.0:5000/api/v1"

def register_user(email: str, password: str) -> None:
    """Register a new user"""
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert response.json().get("email") == email, "Email does not match"

def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with wrong password"""
    url = f"{BASE_URL}/auth_session/login"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def log_in(email: str, password: str) -> str:
    """Log in with correct credentials"""
    url = f"{BASE_URL}/auth_session/login"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    return response.cookies.get("_my_session_id")

def profile_unlogged() -> None:
    """Attempt to get profile without being logged in"""
    url = f"{BASE_URL}/users/me"
    response = requests.get(url)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"

def profile_logged(session_id: str) -> None:
    """Get profile while logged in"""
    url = f"{BASE_URL}/users/me"
    cookies = {"_my_session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def log_out(session_id: str) -> None:
    """Log out the current session"""
    url = f"{BASE_URL}/auth_session/logout"
    cookies = {"_my_session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def reset_password_token(email: str) -> str:
    """Get a reset password token"""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    return response.json().get("reset_token")

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password with the reset token"""
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# Define constants for the test
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
