from __future__ import annotations

from app.schemas.content import Modifier, SceneAction
from app.schemas.game import GameStats


def clamp(value: int) -> int:
    return max(0, min(10, value))


def apply_action(stats: GameStats, action: SceneAction) -> GameStats:
    return GameStats(
        progress=clamp(stats.progress + action.effects.progress_delta),
        risk=clamp(stats.risk + action.effects.risk_delta),
        reputation=clamp(stats.reputation + action.effects.reputation_delta),
        resource=clamp(stats.resource + action.effects.resource_delta),
    )


def apply_modifier(modifier: Modifier, before: GameStats, after: GameStats, action: SceneAction) -> GameStats:
    s = after.model_copy()
    label = action.label.lower()
    mid = modifier.id

    if mid == "lost_voice" and any(k in label for k in ["убед", "договор", "успоко"]):
        s.reputation = clamp(s.reputation - 1)
    if mid == "no_lie" and any(k in label for k in ["блеф", "обвин", "обман"]):
        s.risk = clamp(s.risk + 1)
    if mid == "visible_to_all" and "спрят" in label:
        s.risk = clamp(s.risk + 1)
    if mid == "visible_to_all" and any(k in label for k in ["публич", "питч", "выступ"]):
        s.reputation = clamp(s.reputation + 1)
    if mid == "no_last_resource" and before.resource == 1 and action.effects.resource_delta < 0:
        s.resource = 1
        s.risk = clamp(s.risk + 1)
    if mid == "rush_always":
        s.risk = clamp(s.risk + 1)
    if mid == "reputation_dependent" and s.reputation < before.reputation:
        s.risk = clamp(s.risk + 1)
    return s
