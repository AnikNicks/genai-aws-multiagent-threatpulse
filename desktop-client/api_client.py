import requests
from config import API_URL

class ApiClient:
    @staticmethod
    def get_status():
        return requests.get(f"{API_URL}/status", timeout=10).json()
    
    @staticmethod
    def submit_setup(payload):
        return requests.post(f"{API_URL}/setup", json=payload, timeout=10).json()
    
    @staticmethod
    def fetch_alerts():
        # FIX: Appended () to evaluate the json parsing engine before fetching keys
        return requests.get(f"{API_URL}/alerts", timeout=10).json().get('alerts', [])
    
    @staticmethod
    def trigger_action(alert_id, action, context_payload=None):
        if context_payload is None:
            context_payload = {}
        payload = {"action": action, **context_payload}
        return requests.post(f"{API_URL}/alert/{alert_id}/action", json=payload, timeout=10).json()
    
    @staticmethod
    def purge_system():
        return requests.delete(f"{API_URL}/reset", timeout=10).json()