import customtkinter as ctk
import time
from api_client import ApiClient
from view_drilldown import DrilldownPanel

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, state_obj, reset_handshake_callback):
        super().__init__(parent, fg_color="#0B0F19")
        self.state_obj = state_obj
        self.reset_handshake_callback = reset_handshake_callback
        
        # Grid layout allocation configurations
        self.grid_columnconfigure(0, weight=2) # cascading feed panel
        self.grid_columnconfigure(1, weight=3) # operations drilldown hub
        self.grid_rowconfigure(0, weight=1)
        
        # Left container stack layout frame panel component
        self.left_panel = ctk.CTkFrame(self, fg_color="#0B0F19")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Dynamic system time clock visual header display
        self.time_lbl = ctk.CTkLabel(self.left_panel, text="", font=("Courier", 28, "bold"), text_color="#ffffff")
        self.time_lbl.pack(pady=10, anchor="w")
        
        # Kick off the active live engine ticker loop
        self.update_live_clock()
        
        # Scrollable target container stack feed window frame component
        self.feed_scroll = ctk.CTkScrollableFrame(self.left_panel, fg_color="#0F172A", label_text="ACTIVE THREAT PULSE STREAM TELEMETRY FEED")
        self.feed_scroll.pack(fill="both", expand=True, pady=10)
        
        # Right deep-dive operations drilldown panel hub
        self.right_workspace = ctk.CTkFrame(self, fg_color="#0B0F19")
        self.right_workspace.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        
        # --- OPERATIONAL CONTROL BUTTONS PANEL ---
        ctrl_buttons_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        ctrl_buttons_frame.pack(fill="x", pady=5)
        
        # FIX: Manual Sync trigger button to instantly poll backend without waiting
        self.btn_sync = ctk.CTkButton(
            ctrl_buttons_frame, 
            text="🔄 SYNC LIVE TELEMETRY STREAM", 
            fg_color="#2563eb", 
            hover_color="#1d4ed8", 
            font=("Arial", 12, "bold"),
            command=self.load_alerts_feed
        )
        self.btn_sync.pack(fill="x", pady=5)
        
        # Destructive system purge lifecycle management operational utilities interface switch layout component button control
        ctk.CTkButton(
            ctrl_buttons_frame, 
            text="☢ PURGE ARCHITECTURE SYSTEM RESET ENGINE STATE", 
            fg_color="#7f1d1d", 
            hover_color="#991b1b", 
            font=("Arial", 12, "bold"),
            command=self.destructive_reset
        ).pack(fill="x", pady=5)

        # Trigger initial telemetric fetch & engage background polling daemon
        self.start_telemetry_polling_loop()
        
    def update_live_clock(self):
        current_date_str = time.strftime("%b %d, %A")
        current_time_str = time.strftime("%H:%M:%S")
        self.time_lbl.configure(text=f"{current_time_str} | {current_date_str}")
        self.after(1000, self.update_live_clock)
        
    def start_telemetry_polling_loop(self):
        """FIX: Automatic background engine daemon that requests new threat intelligence logs every 15 seconds"""
        self.load_alerts_feed()
        # Schedule the next network check iteration path (15,000 milliseconds)
        self.after(15000, self.start_telemetry_polling_loop)
        
    def load_alerts_feed(self):
        # Visually indicate syncing behavior on the control button UI
        self.btn_sync.configure(text="⚡ SYNCING INTEL STREAM...", state="disabled")
        self.update_idletasks()
        
        # Clean down existing interface widgets safely inside the scroll pane
        for widget in self.feed_scroll.winfo_children():
            widget.destroy()
        
        try:
            alerts = ApiClient.fetch_alerts()
            
            if isinstance(alerts, dict):
                self.state_obj.active_alerts = alerts.get('alerts', [])
            elif isinstance(alerts, list):
                self.state_obj.active_alerts = alerts
            else:
                self.state_obj.active_alerts = []
                
            print(f"📡 Telemetry Stream Sync: {len(self.state_obj.active_alerts)} active alerts parsed from AWS stack layer.")
            
        except Exception as network_err:
            print(f"❌ Telemetry Sync Error: {network_err}")
            self.render_status_card("FAIL", f"Pipeline Sync Failure: Unable to bind to live stream.\n{network_err}", "#ef4444")
            self.btn_sync.configure(text="🔄 SYNC LIVE TELEMETRY STREAM", state="normal")
            return

        # Handle empty live queue explicitly while agents process background tasks
        if not self.state_obj.active_alerts:
            self.render_status_card("ONLINE", "Threat telemetry matrix clear.\nBackground OSINT agents crawling target data pipeline...", "#10b981")
            self.btn_sync.configure(text="🔄 SYNC LIVE TELEMETRY STREAM", state="normal")
            return
        
        # Render live threats
        for alert in self.state_obj.active_alerts:
            category = alert.get('category', 'INFO')
            state = alert.get('state', 'active')
            desc = alert.get('primary_description', 'No descriptive telemetry metadata available.')
            
            border_color = "#374151" 
            if state == 'resolved': 
                border_color = "#10b981"
            elif state == 'assigned': 
                border_color = "#3b82f6"
            elif category == 'CRITICAL': 
                border_color = "#ef4444"
            
            card = ctk.CTkFrame(self.feed_scroll, fg_color="#1e293b", border_color=border_color, border_width=2, corner_radius=8)
            card.pack(fill="x", pady=8, padx=5)
            
            lbl_txt = f"[{category}] - {desc}\nStatus: {state.upper()}"
            lbl = ctk.CTkLabel(card, text=lbl_txt, font=("Arial", 13, "bold"), justify="left", anchor="w")
            lbl.pack(fill="x", padx=15, pady=15)
            
            lbl.bind("<Button-1>", lambda e, a=alert: self.open_incident_drilldown(a))
            card.bind("<Button-1>", lambda e, a=alert: self.open_incident_drilldown(a))
            
        # Re-enable the manual sync control mechanism safely
        self.btn_sync.configure(text="🔄 SYNC LIVE TELEMETRY STREAM", state="normal")

    def render_status_card(self, status_type, message, color):
        card = ctk.CTkFrame(self.feed_scroll, fg_color="#111827", border_color=color, border_width=1, corner_radius=8)
        card.pack(fill="x", pady=20, padx=10)
        lbl = ctk.CTkLabel(card, text=f"[{status_type}] {message}", font=("Courier", 12, "bold"), text_color=color, justify="center")
        lbl.pack(padx=20, pady=20)
            
    def open_incident_drilldown(self, alert_model):
        for widget in self.right_workspace.winfo_children():
            widget.destroy()
            
        self.state_obj.selected_alert = alert_model
        drilldown = DrilldownPanel(self.right_workspace, alert_model, self.state_obj, self.load_alerts_feed)
        drilldown.pack(fill="both", expand=True)
    
    def destructive_reset(self):
        try:
            ApiClient.purge_system()
        except Exception as e:
            print(f"Purge request skipped or offline: {e}")
        self.reset_handshake_callback()