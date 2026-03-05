from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class TelemetryPoint:
    timestamp: datetime
    domain: str
    asset_id: str
    lat: float
    lon: float
    alt: float
    speed: float
    heading: float
    uncertainty: float = 0.0
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class IntelligenceRecord:
    event_time: datetime
    source_url: str
    title: str
    summary: str
    entities: list[str]
    risk_score: float
    lat: float
    lon: float
    llm_analysis: str


@dataclass
class LayerToggle:
    key: str
    label: str
    enabled: bool
    domain: str


@dataclass
class FeatureConfig:
    live_mode: bool
    recorded_mode: bool
    playback_speed_options: list[float]
    mgrs_enabled: bool
    layers: list[LayerToggle]


@dataclass
class LlmSynthesisResult:
    title: str
    summary: str
    entities: list[str]
    risk_score: float
    lat: float
    lon: float
    llm_analysis: str
    raw: dict[str, Any]
