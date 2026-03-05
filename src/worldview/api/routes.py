from fastapi import APIRouter, Query

from worldview.core.schemas import (
    ProviderCatalogResponse,
    RequiredKeysResponse,
    DomainSummaryResponse,
)
from worldview.core.services import (
    get_providers,
    get_domain_counts,
    get_required_keys,
    get_domain_summary,
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
