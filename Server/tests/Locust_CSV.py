import subprocess

locust_command = [
    "locust",
    "-f", "test_APP.py",
    "--csv=high_peak_test_result",
    "--host= http://10.27.117.57:8013"
]

subprocess.run(locust_command)
