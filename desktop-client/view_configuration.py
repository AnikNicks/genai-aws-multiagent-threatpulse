import customtkinter as ctk
from api_client import ApiClient

class ConfigurationView(ctk.CTkFrame):
    def __init__(self, parent, state_obj, bootstrap_callback):
        super().__init__(parent, fg_color="#0B0F19")
        self.state_obj = state_obj
        self.bootstrap_callback = bootstrap_callback
        
        ctk.CTkLabel(self, text="COGNITIVE THREAT PULSE SYSTEM PROVISIONING PANEL", font=("Courier", 22, "bold"), text_color="#3b82f6").pack(pady=40)
        
        form_frame = ctk.CTkFrame(self, fg_color="#111827", border_color="#1f2937", border_width=2)
        form_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(form_frame, text="Target Corporate Profile Name:", font=("Arial", 14)).pack(pady=(20,5), padx=40, anchor="w")
        self.entry_company = ctk.CTkEntry(form_frame, width=400, fg_color="#1f2937", border_color="#374151") 
        self.entry_company.pack(pady=5, padx=40, anchor="w")
        
        ctk.CTkLabel(form_frame, text="Security Operations Control Center Target Email Notification Address:", font=("Arial", 14)).pack(pady=(20,5), padx=40, anchor="w")
        self.entry_email = ctk.CTkEntry(form_frame, width=400, fg_color="#1f2937", border_color="#374151")
        self.entry_email.pack(pady=5, padx=40, anchor="w")

        ctk.CTkLabel(form_frame, text="Dynamic Platform Threat Feed Refresh Harvesting Interval Scaling Rate:", font=("Arial", 14)).pack(pady=(20,5), padx=40, anchor="w")
        self.dropdown_rate = ctk.CTkOptionMenu(form_frame, values=["15 Min", "1 Hour", "12 Hours", "24 Hours"], fg_color="#1f2937", button_color="#3b82f6")
        self.dropdown_rate.pack(pady=5, padx=40, anchor="w")

        ctk.CTkButton(
            self, 
            text="Initialize Native Active Monitoring Network Engine", 
            font=("Arial", 16, "bold"), 
            fg_color="#10b981", 
            hover_color="#059669", 
            height=50, 
            command=self.execute_provisioning
        ).pack(pady=40)
        
    def execute_provisioning(self):
        payload = {
            "company_name": self.entry_company.get(),
            "target_email": self.entry_email.get(),
            "refresh_rate": self.dropdown_rate.get(),
            "toggles": {"critical": True, "high": True, "medium": True, "low": False}
        }
        
        try:
            # Send the payload down to the server engine
            ApiClient.submit_setup(payload)
        except Exception as api_fallback_error:
            print(f"⚠️ API pipeline offline. Local client state generation triggered directly: {api_fallback_error}")
            
        # Commit configurations locally to the runtime state object anyway
        self.state_obj.company_name = payload["company_name"]
        self.state_obj.refresh_rate = payload["refresh_rate"]
        
        # FIX: Pass True to trigger forced bypass routing straight onto the dashboard workspace frame
        self.bootstrap_callback(forced_bypass=True)