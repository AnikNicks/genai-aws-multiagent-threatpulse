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
        
        # initiate zero-state stateless data verification protocol network handshake execution runtime loop
        self.execute_initialization_handshake()
        
    def execute_initializaiton_handshake(self):
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
            print(f"AWS Network Backend unavailable. Standard offline initialization initialization bypass triggered: {system_fault_error}")
            self.render_configuration_workspace()
    
    def render_configuration_workspace(self):
        if self.active_rendered_view: self.active_rendered_view.destroy()
        self.active_rendered_view = DashboardView(self, self.app_state, self.execute_initializaiton_handshake)
        self.active_rendered_view.pack(fill="both", expand=True)
        
if __name__ == "__main__":
    app_instance = CoreThreatPulseApplicationHub()
    app_instance.mainloop()