from collections import Counter, defaultdict
from datetime import datetime, timezone

from worldview.providers import PROVIDERS, required_env_vars
from worldview.data.mock_data import seed_telemetry, seed_intelligence_records, default_feature_config
from worldview.domain.models import LlmSynthesisResult

TELEMETRY = seed_telemetry()
INTEL_RECORDS = seed_intelligence_records()
FEATURE_CONFIG = default_feature_config()
from worldview.providers import PROVIDERS, required_env_vars


def get_providers(domain: str | None = None, free_tier: bool | None = None) -> list[dict]:
    items = [p.__dict__ for p in PROVIDERS]
    if domain:
        items = [p for p in items if p["domain"] == domain]
    if free_tier is not None:
        items = [p for p in items if p["free_tier"] == free_tier]
    return items


def get_domain_counts() -> dict[str, int]:
    return dict(sorted(Counter(p.domain for p in PROVIDERS).items()))


def get_required_keys() -> list[str]:
    return required_env_vars()


def get_domain_summary() -> list[dict]:
    grouped = defaultdict(list)
    for provider in PROVIDERS:
        grouped[provider.domain].append(provider)

    summary = []
    for domain, items in sorted(grouped.items()):
        free_count = sum(1 for p in items if p.free_tier)
        summary.append(
            {
                "domain": domain,
                "total": len(items),
                "free_tier": free_count,
                "paid_only": len(items) - free_count,
            }
        )
    return summary


def playback_telemetry(start_time: datetime, end_time: datetime, bbox: list[float], domains: list[str]) -> list[dict]:
    lon_min, lat_min, lon_max, lat_max = bbox
    requested_domains = set(domains) if domains else None
    out: list[dict] = []
    for point in TELEMETRY:
        if point.timestamp < start_time or point.timestamp > end_time:
            continue
        if requested_domains and point.domain not in requested_domains:
            continue
        if not (lat_min <= point.lat <= lat_max and lon_min <= point.lon <= lon_max):
            continue
        out.append(point.__dict__)
    return out


def get_live_snapshot(domains: list[str] | None = None) -> list[dict]:
    latest_by_asset: dict[str, dict] = {}
    requested_domains = set(domains) if domains else None
    for point in TELEMETRY:
        if requested_domains and point.domain not in requested_domains:
            continue
        current = latest_by_asset.get(point.asset_id)
        if current is None or point.timestamp > current["timestamp"]:
            latest_by_asset[point.asset_id] = point.__dict__
    return sorted(latest_by_asset.values(), key=lambda x: (x["domain"], x["asset_id"]))


def list_intelligence_records() -> list[dict]:
    return sorted([r.__dict__ for r in INTEL_RECORDS], key=lambda x: x["event_time"], reverse=True)


def get_feature_config() -> dict:
    return {
        "live_mode": FEATURE_CONFIG.live_mode,
        "recorded_mode": FEATURE_CONFIG.recorded_mode,
        "playback_speed_options": FEATURE_CONFIG.playback_speed_options,
        "mgrs_enabled": FEATURE_CONFIG.mgrs_enabled,
        "layers": [layer.__dict__ for layer in FEATURE_CONFIG.layers],
    }


def synthesize_news_event(source_url: str, title: str, body: str) -> dict:
    lowered = body.lower()
    risk = 0.2
    tags = []
    if "protest" in lowered or "conflict" in lowered:
        risk += 0.4
        tags.append("civil_unrest")
    if "jam" in lowered or "spoof" in lowered or "gps" in lowered:
        risk += 0.3
        tags.append("gnss_interference")
    if "military" in lowered:
        risk += 0.2
        tags.append("military_activity")

    result = LlmSynthesisResult(
        title=title,
        summary=body[:180],
        entities=sorted(set(tags)) or ["general_event"],
        risk_score=min(1.0, round(risk, 2)),
        lat=32.08 if "port" in lowered else 50.10,
        lon=34.78 if "port" in lowered else 30.10,
        llm_analysis="Rule-based synthesis placeholder; replace with OpenRouter/OpenAI orchestration.",
        raw={
            "model": "rule-based-placeholder",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_url": source_url,
        },
    )
    return result.__dict__


def to_mgrs(lat: float, lon: float) -> str:
    # Lightweight placeholder; use a true converter (e.g., geographiclib) in production.
    lat_band = "N" if lat >= 0 else "S"
    return f"{abs(int(lat * 10)):03d}{lat_band} {abs(int(lon * 10)):04d}"
