from datetime import datetime, timedelta, timezone

from worldview.domain.models import TelemetryPoint, IntelligenceRecord, LayerToggle, FeatureConfig


def seed_telemetry() -> list[TelemetryPoint]:
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    points: list[TelemetryPoint] = []
    assets = [
        ("aviation", "FLT-001", 51.4700, -0.4543, 32000, 460, 91),
        ("aviation", "MIL-907", 50.1000, 30.1000, 28000, 520, 120),
        ("marine", "IMO-948001", 37.95, 23.64, 0, 18, 45),
        ("satellite", "SAT-25544", 12.2, -70.1, 408000, 27500, 77),
        ("gps_jam", "JAM-001", 32.08, 34.78, 0, 0, 0),
        ("rail", "RAIL-UK-120", 51.52, -0.12, 0, 72, 83),
    ]
    for i in range(60):
        t = now - timedelta(minutes=59 - i)
        for domain, asset_id, lat, lon, alt, speed, heading in assets:
            drift = i * 0.01
            points.append(
                TelemetryPoint(
                    timestamp=t,
                    domain=domain,
                    asset_id=asset_id,
                    lat=lat + (drift if domain in {"aviation", "marine", "rail"} else 0),
                    lon=lon + (drift if domain in {"aviation", "marine", "rail"} else 0),
                    alt=alt,
                    speed=speed,
                    heading=heading,
                    uncertainty=0.9 if domain == "gps_jam" else 0.2,
                    metadata={"source": "mock", "type": domain},
                )
            )
    return points


def seed_intelligence_records() -> list[IntelligenceRecord]:
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    return [
        IntelligenceRecord(
            event_time=now - timedelta(minutes=20),
            source_url="https://example.com/news/port-delay",
            title="Port delays reported amid GPS interference",
            summary="Shipping delay reports correlate with elevated GNSS uncertainty.",
            entities=["Port Authority", "Freight Union"],
            risk_score=0.78,
            lat=32.08,
            lon=34.78,
            llm_analysis="Likely logistics disruption with possible EW activity.",
        ),
        IntelligenceRecord(
            event_time=now - timedelta(minutes=10),
            source_url="https://example.com/news/air-exercise",
            title="Military air exercise announced",
            summary="Regional defense ministry confirms aerial drill window.",
            entities=["Defense Ministry"],
            risk_score=0.62,
            lat=50.1,
            lon=30.1,
            llm_analysis="Planned military activity; monitor adjacent civilian flight reroutes.",
        ),
    ]


def default_feature_config() -> FeatureConfig:
    layers = [
        LayerToggle("commercial_flights", "Commercial Flights", True, "aviation"),
        LayerToggle("military_flights", "Military Flights", True, "aviation"),
        LayerToggle("maritime", "Maritime Traffic", True, "marine"),
        LayerToggle("satellites", "Imaging Satellites", True, "satellite"),
        LayerToggle("gps_jamming", "GPS Jamming", True, "gps_jam"),
        LayerToggle("rail", "Rail", False, "rail"),
    ]
    return FeatureConfig(
        live_mode=True,
        recorded_mode=True,
        playback_speed_options=[0.5, 1.0, 2.0, 5.0],
        mgrs_enabled=True,
        layers=layers,
    )
