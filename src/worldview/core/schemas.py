from datetime import datetime
from typing import List, Dict, Any

from pydantic import BaseModel, Field
from typing import List, Dict
from pydantic import BaseModel


class ProviderModel(BaseModel):
    name: str
    domain: str
    auth: str
    env_vars: List[str]
    free_tier: bool


class ProviderCatalogResponse(BaseModel):
    total: int
    domains: Dict[str, int]
    providers: List[ProviderModel]


class RequiredKeysResponse(BaseModel):
    count: int
    env_vars: List[str]


class DomainSummaryItem(BaseModel):
    domain: str
    total: int
    free_tier: int
    paid_only: int


class DomainSummaryResponse(BaseModel):
    total_domains: int
    items: List[DomainSummaryItem]


class TelemetryPlaybackRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    bbox: List[float] = Field(default_factory=lambda: [-180, -90, 180, 90])
    domains: List[str] = Field(default_factory=list)


class TelemetryPointResponse(BaseModel):
    timestamp: datetime
    domain: str
    asset_id: str
    lat: float
    lon: float
    alt: float
    speed: float
    heading: float
    uncertainty: float
    metadata: Dict[str, str]


class TelemetryPlaybackResponse(BaseModel):
    total: int
    points: List[TelemetryPointResponse]


class IntelligenceRecordResponse(BaseModel):
    event_time: datetime
    source_url: str
    title: str
    summary: str
    entities: List[str]
    risk_score: float
    lat: float
    lon: float
    llm_analysis: str


class LayerToggleResponse(BaseModel):
    key: str
    label: str
    enabled: bool
    domain: str


class FeatureConfigResponse(BaseModel):
    live_mode: bool
    recorded_mode: bool
    playback_speed_options: List[float]
    mgrs_enabled: bool
    layers: List[LayerToggleResponse]


class NewsSynthesisRequest(BaseModel):
    source_url: str
    title: str
    body: str


class NewsSynthesisResponse(BaseModel):
    title: str
    summary: str
    entities: List[str]
    risk_score: float
    lat: float
    lon: float
    llm_analysis: str
    raw: Dict[str, Any]
