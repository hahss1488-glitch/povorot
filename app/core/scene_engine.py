from __future__ import annotations

import random

from app.schemas.content import Scene

PHASES = ["opening", "pressure", "twist", "finale"]


def pick_scene(scenes: list[Scene], blueprint: str, turn_number: int, used_scene_ids: set[str]) -> Scene:
    phase = PHASES[min(turn_number, 3)]
    pool = [s for s in scenes if s.blueprint == blueprint and s.phase == phase and s.id not in used_scene_ids]
    if not pool:
        pool = [s for s in scenes if s.blueprint == blueprint and s.phase == phase]
    return random.choice(pool)
