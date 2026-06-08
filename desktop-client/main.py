import customtkinter as ctk
from view_configuration import ConfigurationView
from view_dashboard import DashboardView
from config import ClientState

class CoreThreatPulseApplicationHub(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GENAI THREAT & OSINT INTELLIGENCE COCKPIT (ENTERPRISE AWS STACK EDITION)")
        self.geometry("1300x850")
        ctk.set_appearance_mode("dark")
        
        self.app_state = ClientState()
        self.active_rendered_view = None
        
        # Initial cold boot handshake check
        self.execute_initialization_handshake()
        
    def execute_initialization_handshake(self, forced_bypass=False):
        # FIX: Explicitly check if we are forcing a dashboard view render after a successful setup submission
        if forced_bypass:
            print("⚡ [BYPASS] Onboarding submitted successfully. Forcing transition to active dashboard panel...")
            self.render_dashboard_workspace()
            return

        try:
            from api_client import ApiClient
            response_data = ApiClient.get_status()
            if response_data.get('active', False):
                self.app_state.company_name = response_data.get('company_name')
                self.app_state.refresh_rate = response_data.get('refresh_rate')
                self.render_dashboard_workspace()
            else:
                self.render_configuration_workspace()
        except Exception as system_fault_error:
            print(f"AWS Network Backend unavailable. Standard offline initialization bypass triggered: {system_fault_error}")
            self.render_configuration_workspace()
            
    def render_dashboard_workspace(self):
        if self.active_rendered_view: 
            self.active_rendered_view.destroy()
        self.active_rendered_view = DashboardView(self, self.app_state, self.execute_initialization_handshake)
        self.active_rendered_view.pack(fill="both", expand=True)
    
    def render_configuration_workspace(self):
        if self.active_rendered_view: 
            self.active_rendered_view.destroy()
        self.active_rendered_view = ConfigurationView(self, self.app_state, self.execute_initialization_handshake)
        self.active_rendered_view.pack(fill="both", expand=True)
        
if __name__ == "__main__":
    app_instance = CoreThreatPulseApplicationHub()
    app_instance.mainloop()