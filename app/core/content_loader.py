from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.schemas.content import ContentPack


CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def _load_json(filename: str) -> Any:
    with (CONTENT_DIR / filename).open("r", encoding="utf-8") as f:
        return json.load(f)


def load_content() -> ContentPack:
    return ContentPack(
        items=_load_json("items.json"),
        locations=_load_json("locations.json"),
        fears=_load_json("fears.json"),
        roles=_load_json("roles.json"),
        threats=_load_json("threats.json"),
        modifiers=_load_json("modifiers.json"),
        blueprints=_load_json("blueprints.json"),
        scenes=_load_json("scenes.json"),
        endings=_load_json("endings.json"),
        common_names=_load_json("common_names.json"),
        title_words=_load_json("title_words.json"),
        aliases=_load_json("aliases.json"),
        intents=_load_json("intents.json"),
    )
