from apistar.test import TestClient
flight_endpoint = '/task/'
def test_add_flight(client):
    response = client.post(task_endpoint, new_task)
    assert response.status_code == 201

    assert response.json() == added_task
