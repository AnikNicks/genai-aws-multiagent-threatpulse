import customtkinter as ctk
import time
from api_client import ApiClient
from view_drilldown import DrilldownPanel

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, state_obj, reset_handshake_callback):
        super().__init__(parent, fg_color="0B0F19")
        self.state_obj = state_obj
        self.reset_handshake_callback = reset_handshake_callback
        
        # config structure grid spitter
        self.grid_columnconfigure(0, weight=2) # cascadeing lock-screen feed
        self.grid_columnconfigure(1, weight=3) # drilldown and cartography maps
        self. grid_rowconfigure(0, weight=1)
        
        #left container stack layout frame panel component
        self.left_panel = ctk.CTkFrame(self, fg_color="0B0F19")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # dynamic system time clock visual header display
        current_date_str = time.strftime("%b %d, %A")
        current_time_str = time.strftime("%H:%M")
        time_lbl = ctk.CTkLabel(self.left_panel, text =f"{current_time_str} | {current_date_str}", font=("Courier", 28, "bold"), text_color="#ffffff")
        time_lbl.pack(pady=10, anchor="w")
        
        # scrollable target container stack feed window frame component
        self.feed_scroll = ctk.CTkScrollableFrame(self.left_panel, fg_color="#0F172A", label_text="ACTIVE THREAT PULSE STREAM TELEMETRY FEED")
        self.feed_scroll.pack(fill="both", expand=True, pady=10)
        
        # right deep-dive operations drilldown panel hub
        self.right_workspace = ctk.CTkFrame(self, fg_color="#0B0F19")
        self.right_workspace.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        
        # Destructive system purge lifecycle management operational utilities interface switch layout component button control
        ctk.CTkButton(self.left_panel, text="☢ PURGE ARCHITECTURE SYSTEM RESET ENGINE STATE", fg_color="#7f1d1d", hover_color="#991b1b", command=self.destructive_reset).pack(fill="x", pady=10)

        self.load_alerts_feed()
        
        def load_alerts_feed():
            for widget in self.feed_scroll.winfo_children():
                widget.destroy()
            
            self.state_obj.active_alerts = ApiClient.fetch_alerts()
            for alert in self.state_obj.active_alerts:
                # endforce dynamic reactive color schemas
                border_color = "#374151" # Default active baseline border configuration
            if alert.get('state') == 'resolved': border_color = "#10b981"
            elif alert.get('state') == 'assigned': border_color = "#3b82f6"
            elif alert.get('category') == 'CRITICAL': border_color = "#ef4444"
            
            card = ctk.CTkFrame(self.feed_scroll, fg_color="#1e293b", border_color=border_color, border_width=2, corner_radius=8)
            card.pack(fill="x", pady=8, padx=5)
            
            lbl_txt = f"[{alert['category']}] - {alert['primary_description']}\nState Status Indicator: {alert['state'].upper()}"
            lbl = ctk.CTkLabel(card, text=lbl_txt, font=("Arial", 13, "bold"), justify="left", anchor="w")
            lbl.pack(fill="x", padx=15, pady=15)
            
            # bind client interaction selectors natively
            lbl.bind("<Button-1", lambda e, a=alert: self.open_inciident_drilldown(a))
            card.bind("<Button-1>", lambda e, a=alert: self.open_incident_drilldown(a))
            
        def open_incident_drilldown(self, alert_model):
            for widget in self.right_workspace.winfo_children():
                widget.destroy()
                
            self.state_obj.selected_alert = alert_model
            drilldown = DrilldownPanel(self.right_workspace, alert_model, self.state_obj, self.load_alerts_feed)
            drilldown.pack(fill="both", expand=True)
        
        def destructive_reset(self):
            ApiClient.purge_system()
            self.reset_handshake_callback()