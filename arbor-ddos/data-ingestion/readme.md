# Arbor DDoS

## Data Ingestion

This is one of the ways that I found to receive Arbor Alerts on FortiSOAR. You need to execute this Python script on a zombie machine using cron to send the JSON from the alerts to FortiSOAR using the API.

* You will need to generate an Arbor API Token:

![image](https://github.com/tutueh/fortisoar/assets/85353380/18a6474f-de8d-47eb-a023-87b03013ecfa)

* **Playbook:**

![image](https://github.com/tutueh/fortisoar/assets/85353380/eec06271-8330-41b5-8041-b48a56eb9e89)
