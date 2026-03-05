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
