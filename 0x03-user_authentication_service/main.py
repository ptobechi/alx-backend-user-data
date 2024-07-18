import requests

BASE_URL = 'http://localhost:5000'  # Replace with your actual server URL

def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print(f"User {email} registered successfully.")

def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/sessions"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 401
    print(f"Attempted login with wrong password for {email} returned 401 as expected.")

def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print(f"Logged in successfully as {email}.")
    return response.cookies.get('session_id')

def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403
    print("Attempted to access profile unlogged, returned 403 as expected.")

def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    print(f"Accessed profile successfully with session_id {session_id}.")

def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    print(f"Logged out successfully with session_id {session_id}.")

def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    reset_token = response.json()['reset_token']
    print(f"Reset password token generated successfully for {email}: {reset_token}.")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    print(f"Password updated successfully for {email}.")

# Main script
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
