from pydantic import BaseModel, Field
from typing import List, Optional

class LocationMetric(BaseModel):
    lat: float
    lon: float
    city: Optional[str] = None
    country: Optional[str] = None

class ThreatAlertSchema(BaseModel):
    alert_id: str
    company_name: str
    threat_severity: int
    category: str
    primary_description: str
    trigger_date: List[str]
    affected_nodes: List[str]
    affected_nodes: List[str]
    ai_insight: str
    recommendations: List[str]
    localized_locations: List[LocationMetric] = []
    distributed_locations: List[LocationMetric] = []
    state: str = "active"
    assigned_to = Optional[str] = None