import subprocess
from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task(1)
    def get_root(self):
        self.client.get("/")

    @task(2)
    def read_lines(self):
        self.client.get("/lines/1号线")

    @task(3)
    def read_stations(self):
        self.client.get("/stations/Luohu")

    @task(4)
    def p_board(self):
        self.client.post("/p_board/administrators/Tanglang")

    @task(5)
    def p_alight(self):
        self.client.post("/p_alight/administrators/Tanglang/Chiwei")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)


if __name__ == "__main__":
    import sys

    locust_command = [
        sys.executable, "-m", "locust",
        "-f", __file__,
        "--csv=high_peak_test_result",
        "--host=http://10.27.117.57:8013"

    ]

    subprocess.run(locust_command)
