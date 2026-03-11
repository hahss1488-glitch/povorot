from __future__ import annotations

from typing import TypeVar

from rapidfuzz import fuzz

from app.schemas.content import EntityBase, MatchResult

T = TypeVar("T", bound=EntityBase)


def _all_names(entity: T) -> list[str]:
    return [entity.name, *entity.aliases]


def match_entity(user_input: str, entities: list[T]) -> MatchResult:
    text = user_input.strip()
    text_lower = text.lower()

    for entity in entities:
        if text in _all_names(entity):
            return MatchResult(entity=entity, score=100, matched_by="exact")
    for entity in entities:
        if text_lower in [v.lower() for v in _all_names(entity)]:
            return MatchResult(entity=entity, score=98, matched_by="case-insensitive")

    best_entity = entities[0]
    best_score = -1.0
    for entity in entities:
        scores = [fuzz.WRatio(text_lower, value.lower()) for value in _all_names(entity)]
        score = max(scores)
        if score > best_score:
            best_score = score
            best_entity = entity

    adaptation = None
    if best_score < 90:
        adaptation = f"В этом мире ближе всего нашлась сущность «{best_entity.name}» (адаптация ввода)."
    elif best_score < 97:
        adaptation = f"Я адаптировал ввод к ближайшей сущности: «{best_entity.name}»."

    return MatchResult(entity=best_entity, score=best_score, adaptation_line=adaptation, matched_by="fuzzy")
