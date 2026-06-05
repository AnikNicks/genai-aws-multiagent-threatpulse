import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:3000") # SAM local endpoint

class ClientState:
    def __inti__(self):
        self.company_name = ""
        self.refresh_rate = ""
        self.active_alerts = []
        self.selected_alert = None