import requests

def get_auth_token(email: str, password: str) -> str:
    """Authenticate and retrieve an auth token."""
    login_url = "https://api.dev.laudio.io/auth/login"
    headers = {"x-app-id": "1"}
    data = {"email": email, "password": password}

    response = requests.post(login_url, headers=headers, json=data)
    try:
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.HTTPError as e:
        print(f"[get_auth_token] Error response: {response.text}")
        raise e

    print(f"[get_auth_token] Response Status Code: {response.status_code}")
    return response.json().get("data", {}).get("accessToken")

def get_nudge_data(auth_token: str, employee_id: str) -> dict:
    """Retrieve nudge data for a specific employee."""
    nudge_url = f"https://api.dev.laudio.io/insight/v1/nudge/employee/{employee_id}?status=active"
    headers = {"Authorization": f"Bearer {auth_token}", "x-app-id": "1"}

    response = requests.get(nudge_url, headers=headers)
    print(f"[get_nudge_data] Response Status Code: {response.status_code}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[get_nudge_data] Error response: {response.text}")
        raise e

    return response.json()
