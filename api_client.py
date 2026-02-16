import urllib3
import certifi
import json
import logging

class APIClient:
    def __init__(self, base_url, auth_url, client_id, client_secret):
        self.base_url = base_url
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.cookie = None

        self.http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

    def authenticate(self):
        payload = {
            "clientId": self.client_id,
            "secretKey": self.client_secret,
        }

        url = f"{self.auth_url}/authenticate"

        try:
            r = self.http.request(
                "POST",
                url,
                body=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                timeout=urllib3.Timeout(connect=5, read=30),
            )

            if r.status != 200:
                raise Exception(f"Auth failed: {r.status}")

            self.cookie = r.headers.get("Set-Cookie")
            logging.info("Authentication successful.")

        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            raise

    def fetch_record(self, record_id, fields=None):
        url = f"{self.base_url}/records/{record_id}"
        payload = {"fields": fields or [], "id": record_id}

        try:
            r = self.http.request(
                "POST",
                url,
                body=json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "cookie": self.cookie,
                },
                timeout=urllib3.Timeout(connect=5, read=30),
                retries=2,
            )

            if r.status != 200:
                return {}

            obj = json.loads(r.data)
            return obj.get("response", {}).get("fields", {})

        except Exception as e:
            logging.warning(f"Failed to fetch {record_id}: {e}")
            return {}
