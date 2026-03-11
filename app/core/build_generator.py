from __future__ import annotations

import random

from app.schemas.content import ContentPack, Fear, Item, Location, NameFeatures
from app.schemas.game import BuildResult, GameStats


def clamp(value: int, low: int = 0, high: int = 10) -> int:
    return max(low, min(high, value))


def initial_stats(name: NameFeatures, item: Item, location: Location, fear: Fear) -> GameStats:
    progress = clamp(3 + ((item.utility + location.commerce) // 2), 1, 5)
    risk = clamp(3 + ((location.danger + fear.loss_fear + fear.physical_fear) // 2) - (name.formality // 2), 1, 5)
    reputation = clamp(3 + ((name.formality + location.publicness + item.status) // 2) - (name.oddness // 2), 1, 5)
    resource = clamp(3 + ((item.utility + item.mobility + location.commerce) // 2), 1, 5)
    return GameStats(progress=progress, risk=risk, reputation=reputation, resource=resource)


def choose_by_blueprint(content: ContentPack, blueprint_id: str) -> tuple[str, str, str]:
    roles = [r for r in content.roles if blueprint_id in r.compatible_blueprints]
    threats = [t for t in content.threats if blueprint_id in t.compatible_blueprints]
    modifiers = [m for m in content.modifiers if blueprint_id in m.compatible_blueprints]
    return random.choice(roles).id, random.choice(threats).id, random.choice(modifiers).id


def build_result(
    content: ContentPack,
    blueprint_id: str,
    name: NameFeatures,
    item: Item,
    location: Location,
    fear: Fear,
    adaptation_lines: list[str],
) -> BuildResult:
    role_id, threat_id, modifier_id = choose_by_blueprint(content, blueprint_id)
    stats = initial_stats(name, item, location, fear)
    goal = next(b.goal for b in content.blueprints if b.id == blueprint_id)
    lines = [*name.reasons[:2]]
    if item.utility >= 1:
        lines.append("Предмет практичный — сюжет смещается к прикладным решениям.")
    if location.publicness >= 1:
        lines.append("Локация публичная — репутация становится важнее.")
    if fear.social_fear >= 1:
        lines.append("Страх связан с оценкой окружающих — угроза становится социальной.")
    lines.extend(adaptation_lines)
    return BuildResult(
        blueprint_id=blueprint_id,
        role_id=role_id,
        threat_id=threat_id,
        modifier_id=modifier_id,
        goal=goal,
        explanation_lines=lines[:4],
        stats=stats,
    )
