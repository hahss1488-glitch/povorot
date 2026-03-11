from __future__ import annotations

from rapidfuzz import fuzz

from app.schemas.content import SceneAction


def parse_action(user_text: str, actions: list[SceneAction], intents: dict[str, list[str]]) -> SceneAction:
    text = user_text.strip().lower()
    best = max(actions, key=lambda a: fuzz.WRatio(text, a.label.lower()))
    if fuzz.WRatio(text, best.label.lower()) >= 85:
        return best

    chosen_intent: str | None = None
    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            chosen_intent = intent
            break

    if chosen_intent:
        intent_actions = [a for a in actions if a.intent == chosen_intent]
        if intent_actions:
            return intent_actions[0]

    fallback = next((a for a in actions if a.intent == "импровизировать"), actions[0])
    return fallback
