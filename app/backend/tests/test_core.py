"""Smoke: health + employee CRUD + increment + audit + analytics."""

from datetime import date


def _payload(email="john.doe@acme.local"):
    return {
        "name": "John Doe",
        "email": email,
        "department": "Eng",
        "job_title": "SDE II",
        "country": "IN",
        "currency": "INR",
        "base_salary": "800000.00",
        "bonus": "50000.00",
        "joining_date": "2023-01-15",
    }


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_get_increment_employee(client):
    created = client.post("/employees", json=_payload())
    assert created.status_code == 201, created.text
    emp_id = created.json()["id"]

    fetched = client.get(f"/employees/{emp_id}")
    assert fetched.status_code == 200
    assert fetched.json()["email"] == _payload()["email"]

    inc = client.post(
        f"/employees/{emp_id}/increment",
        json={"percent": 10, "reason": "annual review"},
    )
    assert inc.status_code == 200, inc.text
    assert inc.json()["base_salary"] == "880000.00"


def test_duplicate_email_rejected(client):
    assert client.post("/employees", json=_payload()).status_code == 201
    dup = client.post("/employees", json=_payload())
    assert dup.status_code == 409


def test_list_pagination_and_analytics(client):
    client.post("/employees", json=_payload("a@acme.local"))
    second = _payload("b@acme.local")
    second.update(
        {
            "department": "HR",
            "country": "US",
            "currency": "USD",
            "base_salary": "90000.00",
            "bonus": "5000.00",
        }
    )
    client.post("/employees", json=second)

    listing = client.get("/employees", params={"page": 1, "size": 1})
    assert listing.status_code == 200
    assert listing.json()["meta"]["total"] == 2

    summary = client.get("/analytics/summary")
    assert summary.status_code == 200, summary.text
    body = summary.json()
    assert body["headcount"] == 2
    assert body["total_usd"] is not None
    assert len(body["distribution"]) == 4
