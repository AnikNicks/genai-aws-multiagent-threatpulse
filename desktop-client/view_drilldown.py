import customtkinter as ctk
from tkintermapview import TkinterMapView
from api_client import ApiClient

class DrilldownPanel(ctk.CTkFrame):
    def __init__(self, parent, alert_model, state_client, refresh_dashboard_func):
        super().__init__(parent, fg_color="#111827", border_color="#1f2937", border_width=2, corner_radius=12)
        self.alert = alert_model
        self.app_state = state_client
        self.refresh_dashboard = refresh_dashboard_func
        
        self.grid_columnconfigure(0, weight=1)
        self.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Embedded map core instance container canvas
        map_frame = ctk.CTkFrame(self, height=250)
        map_frame.pack(fill="x", padx=15, pady=15)
        
        self.map_widget = TkinterMapView(map_frame, width=600, height=250, corner_radius=8)
        self.map_widget.pack(fill="both", expand=True)
        self.project_spatial_coordinates()
        
        # Radial risk progress metrics framework tracking header panel row display gauge components
        gauge_frame = ctk.CTkFrame(self, fg_color="transparent")
        gauge_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(gauge_frame, text=f"📊 THREAT INFRASTRUCTURE RISK SEVERITY CRITICAL INDEX ENGINE LEVEL: {self.alert['threat_severity']}%", font=("Courier", 16, "bold"), text_color="#ef4444").pack(anchor="w")
        
        # FIX: Changed ctk.CTkTextBox to ctk.CTkTextbox (lowercase 'b')
        insights_box = ctk.CTkTextbox(self, fg_color="#1f2937", border_color="#374151", border_width=1, font=("Arial", 12), height=180)
        insights_box.pack(fill="both", expand=True, padx=20, pady=10)

        diagnostics_payload = (
            f"👁️ PLATFORM SIGNAL SOURCE ORIGIN EXTRACTED TELEMETRY TARGET PROOFS:\n"
            f"   {', '.join(self.alert['trigger_data'])}\n\n"
            f"👤 CURRENT IMPACTED TARGET ATTACK VECTOR SURFACE NODES INFRASTRUCTURE:\n"
            f"   {', '.join(self.alert['affected_nodes'])}\n\n"
            f"🧠 NATIVE AMAZON BEDROCK EXPLAINABLE INTELLIGENCE COGNITIVE SUMMARY ANALYTICAL ANALYSIS:\n"
            f"   {self.alert['ai_insight']}\n\n"
            f"✅ ACTIONS MANDATED SYSTEM RECOVERY STRATEGIC MANUAL DIRECTIVE RUNBOOKS:\n"
            f"   " + "\n   ".join([f"- {rec}" for rec in self.alert['recommendations']])
        )
        if self.alert.get('assigned_to'):
            diagnostics_payload += f"\n\n✍ SYSTEM ASSIGNED ACCOUNT ROUTED PIPELINE TARGET HOLDER: {self.alert['assigned_to']}"

        insights_box.insert("0.0", diagnostics_payload)
        insights_box.configure(state="disabled")

        # Command Action Bar Framework Operation Matrix Trigger Control Row Components Container
        ctrl_ribbon = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_ribbon.pack(fill="x", side="bottom", padx=20, pady=20)

        ctk.CTkButton(ctrl_ribbon, text="Resolved ✓", fg_color="#10b981", hover_color="#059669", font=("Arial", 13, "bold"), command=self.fire_resolve).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(ctrl_ribbon, text="Assign ✍", fg_color="#3b82f6", hover_color="#2563eb", font=("Arial", 13, "bold"), command=self.fire_assign).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(ctrl_ribbon, text="Reject ✕", fg_color="#ef4444", hover_color="#dc2626", font=("Arial", 13, "bold"), command=self.fire_reject).pack(side="right", padx=5, expand=True, fill="x")

    def project_spatial_coordinates(self):
        locs = self.alert.get('localized_locations', []) or self.alert.get('distributed_locations', [])
        if locs:
            self.map_widget.set_position(locs[0]['lat'], locs[0]['lon'])
            self.map_widget.set_zoom(6 if self.alert.get('localized_locations') else 2)
            for point in locs:
                self.map_widget.set_marker(point['lat'], point['lon'], text=f"Target Event: {point.get('city') or point.get('country')}")
        else:
            self.map_widget.set_position(38.8951, -77.0364)

    def fire_resolve(self):
        ApiClient.trigger_action(self.alert['alert_id'], "resolve")
        self.refresh_dashboard()

    def fire_assign(self):
        input_dialog = ctk.CTkInputDialog(text="Provide target operational engineer assignment routing email address profile:", title="Threat Assignment Configuration Hub Route")
        target_email = input_dialog.get_input()
        if target_email:
            ApiClient.trigger_action(self.alert['alert_id'], "assign", {"email": target_email})
            self.refresh_dashboard()

    def fire_reject(self):
        ApiClient.trigger_action(self.alert['alert_id'], "reject")
        self.refresh_dashboard()
        self.destroy()