import urllib3
import certifi
import json

class APIClient:
    def __init__(self, base_url, auth_url, client_id, client_secret):
        self.base_url = base_url
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.cookie = None
        urllib3.disable_warnings()
        self.http = urllib3.PoolManager(cert_reqs='CERT_NONE', ca_certs=certifi.where())

    def authenticate(self):
        """
        Authenticate and store cookie/session token.
        """
        payload = {
            "clientId": self.client_id,
            "secretKey": self.client_secret
        }
        url = f"{self.auth_url}/authenticate"
        r = self.http.request(
            "POST",
            url,
            body=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        self.cookie = r.info().get_all("Set-Cookie")
        print("🔐 Authentication successful.")

    def fetch_record(self, record_id, fields=None):
        """
        Generic fetch of record data by ID.
        """
        url = f"{self.base_url}/records/{record_id}"
        payload = {"fields": fields or [], "id": record_id}
        r = self.http.request(
            "POST",
            url,
            body=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "cookie": self.cookie[0]}
        )
        obj = json.loads(r.data)
        return obj.get("response", {}).get("fields", {})
