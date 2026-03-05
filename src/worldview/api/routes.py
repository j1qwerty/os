import asyncio
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query, WebSocket

from worldview.core.schemas import (
    ProviderCatalogResponse,
    RequiredKeysResponse,
    DomainSummaryResponse,
    TelemetryPlaybackRequest,
    TelemetryPlaybackResponse,
    IntelligenceRecordResponse,
    FeatureConfigResponse,
    NewsSynthesisRequest,
    NewsSynthesisResponse,
)
from worldview.core.services import (
    get_providers,
    get_domain_counts,
    get_required_keys,
    get_domain_summary,
    playback_telemetry,
    get_live_snapshot,
    list_intelligence_records,
    get_feature_config,
    synthesize_news_event,
    to_mgrs,
)

router = APIRouter(prefix="/api/v1", tags=["worldview"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "worldview"}


@router.get("/providers", response_model=ProviderCatalogResponse)
def providers(
    domain: str | None = Query(default=None, description="Filter by domain"),
    free_tier: bool | None = Query(default=None, description="Filter by free_tier"),
) -> ProviderCatalogResponse:
    items = get_providers(domain=domain, free_tier=free_tier)
    counts = get_domain_counts()
    return ProviderCatalogResponse(total=len(items), domains=counts, providers=items)


@router.get("/providers/required-keys", response_model=RequiredKeysResponse)
def required_keys() -> RequiredKeysResponse:
    env_vars = get_required_keys()
    return RequiredKeysResponse(count=len(env_vars), env_vars=env_vars)


@router.get("/domains/summary", response_model=DomainSummaryResponse)
def domains_summary() -> DomainSummaryResponse:
    items = get_domain_summary()
    return DomainSummaryResponse(total_domains=len(items), items=items)


@router.post("/telemetry/playback", response_model=TelemetryPlaybackResponse)
def telemetry_playback(payload: TelemetryPlaybackRequest) -> TelemetryPlaybackResponse:
    points = playback_telemetry(payload.start_time, payload.end_time, payload.bbox, payload.domains)
    return TelemetryPlaybackResponse(total=len(points), points=points)


@router.get("/telemetry/live")
def telemetry_live(domains: list[str] = Query(default=[])) -> dict:
    items = get_live_snapshot(domains if domains else None)
    return {"total": len(items), "points": items}


@router.get("/intelligence/records", response_model=list[IntelligenceRecordResponse])
def intelligence_records() -> list[IntelligenceRecordResponse]:
    return [IntelligenceRecordResponse(**r) for r in list_intelligence_records()]


@router.get("/features", response_model=FeatureConfigResponse)
def features() -> FeatureConfigResponse:
    return FeatureConfigResponse(**get_feature_config())


@router.post("/intelligence/synthesize", response_model=NewsSynthesisResponse)
def synthesize(payload: NewsSynthesisRequest) -> NewsSynthesisResponse:
    result = synthesize_news_event(payload.source_url, payload.title, payload.body)
    return NewsSynthesisResponse(**result)


@router.get("/geo/mgrs")
def mgrs(lat: float, lon: float) -> dict:
    return {"lat": lat, "lon": lon, "mgrs": to_mgrs(lat, lon)}


@router.websocket("/ws/live")
async def live_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            snapshot = get_live_snapshot()
            await websocket.send_json(
                {
                    "mode": "live",
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "total": len(snapshot),
                    "points": snapshot,
                }
            )
            await asyncio.sleep(2)
    except Exception:
        await websocket.close()


@router.get("/telemetry/default-window")
def telemetry_default_window() -> dict:
    end_time = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    start_time = end_time - timedelta(minutes=30)
    return {
        "start_time": start_time,
        "end_time": end_time,
        "bbox": [-180, -90, 180, 90],
        "domains": ["aviation", "marine", "satellite", "gps_jam"],
    }
