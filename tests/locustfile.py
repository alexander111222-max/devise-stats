import random
import time
from locust import HttpUser, between, task, tag


def create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "testUser",
            "email": f"test{random.randint(1, 100000)}@mail.ru",
            "password": "password",
        },
    )
    if response.status_code != 200:
        return None
    return response.json().get("id")


def create_deviсe(client, user_id: int):
    response = client.post(
        "/devices",
        json={"name": f"Device {random.randint(1, 10000)}", "user_id": user_id},
    )
    if response.status_code != 200:
        return None
    return response.json().get("id")


def generate_measurements(client, devise_id: int):
    for _ in range(10):
        client.post(
            f"/measurements/{devise_id}",
            json={
                "x": random.uniform(-100, 200),
                "y": random.uniform(-100, 200),
                "z": random.uniform(-100, 200),
            },
        )


class WriteUser(HttpUser):
    time_wait = between(0.5, 1.5)
    weight = 5

    def on_start(self):
        self.user_id = create_user(self.client)
        if not self.user_id:
            return
        self.device_id = create_deviсe(self.client, self.user_id)

    @task
    @tag("write")
    def add_measuremente(self):
        if not self.device_id:
            return

        self.client.post(
            f"/measurements/{self.device_id}",
            json={
                "x": random.uniform(-100, 200),
                "y": random.uniform(-100, 200),
                "z": random.uniform(-100, 200),
            },
        )


class ReadUser(HttpUser):
    time_wait = between(1, 3)
    weight = 3

    def on_start(self):
        self.user_id = create_user(self.client)
        if not self.user_id:
            return
        self.device_id = create_deviсe(self.client, self.user_id)
        if not self.device_id:
            return
        generate_measurements(self.client, self.device_id)

    @task(3)
    @tag("read")
    def get_analytics(self):
        if not self.device_id:
            return
        with self.client.get(
            f"/analytics/{self.device_id}", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"analutics fail: {response.status_code}")

    @task(2)
    @tag("read")
    def get_analytics_with_period(self):
        if not self.device_id:
            return
        with self.client.get(
            f"/analytics/{self.device_id}",
            params={
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2026-12-31T00:00:00",
            },
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"analytics with period fail {response.status_code}")

    @task(1)
    @tag("read")
    def get_analytics_with_by_user(self):
        if not self.user_id:
            return

        with self.client.get(
            f"/analytics/users/{self.user_id}", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"user analytics failed: {response.status_code}")


class AsyncAnalyticsUser(HttpUser):
    time_wait = between(1, 3)
    weight = 2

    def on_start(self):
        self.user_id = create_user(self.client)
        if not self.user_id:
            return
        self.device_id = create_deviсe(self.client, self.user_id)
        if not self.device_id:
            return

        generate_measurements(self.client, self.device_id)

    @task
    @tag("async")
    def get_analytics_async(self):
        if not self.device_id:
            return

        with self.client.get(
            f"/analytics/{self.device_id}/async", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"async task start fail: {response.status_code}")
                return
            task_id = response.json().get("task_id")

        if not task_id:
            return

        for attempt in range(30):
            time.sleep(1)
            with self.client.get(
                f"/analytics/tasks/{task_id}", catch_response=True
            ) as result:
                if result.status_code != 200:
                    result.failure(f"poling fal: {result.status_code}")
                    return

                status = result.json().get("status")
                if status == "SUCCESS":
                    break
                if status == "FAILURE":
                    result.failure("task fail")
                    break
