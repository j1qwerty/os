from collections import Counter, defaultdict
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
