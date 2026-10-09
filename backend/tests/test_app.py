from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_login_success():
    response = client.post('/api/v1/auth/bootstrap-admin', params={'email': 'admin@example.com', 'password': 'StrongPass!123', 'full_name': 'Admin User'})
    assert response.status_code == 200
    login = client.post('/api/v1/auth/login', json={'email': 'admin@example.com', 'password': 'StrongPass!123'})
    assert login.status_code == 200
    assert 'access_token' in login.json()


def test_login_failure():
    response = client.post('/api/v1/auth/login', json={'email': 'admin@example.com', 'password': 'wrong'})
    assert response.status_code == 401


def test_public_prediction_mock():
    payload = {
        'observation_date': '2025-03-15',
        'location': 'Anuradhapura',
        'rainfall_mm': 15,
        'temperature_c': 30,
        'humidity_pct': 65,
        'sunshine_hours': 8,
        'soil_temperature_c': 29,
        'wind_speed_kmh': 8,
        'pressure_hpa': 1012,
        'input_type': 'manual',
    }
    response = client.post('/api/v1/evaporation/predict', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['provider_type'] == 'mock'
    assert 'DEMO' not in body['explanation'] or 'demo' in body['explanation'].lower()


def test_water_estimate_formulas():
    response = client.post('/api/v1/water/estimate', json={
        'crop': 'Rice',
        'stage': 'mid-season',
        'etc_mm_day': 5.0,
        'effective_rainfall_mm_day': 2.0,
        'field_area_m2': 1000,
        'irrigation_efficiency': 70,
    })
    assert response.status_code == 200
    body = response.json()
    assert body['net_irrigation_mm_day'] == 3.0
    assert round(body['gross_irrigation_depth_mm'], 2) == 4.29


def test_specialist_access_denied_without_auth():
    client.cookies.clear()
    response = client.get('/api/v1/specialist/dashboard')
    assert response.status_code == 401


def test_admin_access_denied_without_auth():
    client.cookies.clear()
    response = client.get('/api/v1/admin/dashboard')
    assert response.status_code == 401
