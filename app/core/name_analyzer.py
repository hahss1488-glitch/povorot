from __future__ import annotations

import re

from app.schemas.content import NameFeatures


def clamp(value: int, low: int = 0, high: int = 2) -> int:
    return max(low, min(high, value))


def analyze_name(raw_name: str, common_names: list[str], title_words: list[str]) -> NameFeatures:
    normalized = " ".join(raw_name.strip().split())
    tokens = [t for t in normalized.split(" ") if t]
    low = normalized.lower()

    formality = 0
    reasons: list[str] = []
    if normalized and normalized[0].isupper() and not normalized.isupper():
        formality += 1
        reasons.append("Имя начинается с заглавной буквы — это добавляет официальный оттенок.")
    if len(tokens) >= 2 or any(word in low for word in title_words):
        if not normalized.islower() and not normalized.isupper():
            formality += 1
        reasons.append("В имени есть титул или несколько частей — образ звучит формальнее.")

    oddness = 0
    first_token = tokens[0] if tokens else ""
    base_name = first_token.capitalize()
    if base_name not in common_names:
        oddness += 1
        reasons.append("Имя не похоже на частое — мир воспринимает тебя как нестандартного героя.")
    if re.search(r"[-\d\W]", normalized) or (not normalized.islower() and not normalized.isupper() and normalized != normalized.title()):
        oddness += 1
        reasons.append("Форма имени необычная (дефис/символы/смешанный стиль), это повышает странность образа.")

    main_token_len = len(first_token)
    if main_token_len <= 4:
        compactness = 2
    elif main_token_len <= 7:
        compactness = 1
    else:
        compactness = 0

    if compactness == 2:
        reasons.append("Короткое имя помогает действовать быстро.")

    duality = 0
    if len(tokens) >= 2:
        duality = 2
        reasons.append("Имя состоит из нескольких частей — это добавляет двойственность роли.")
    elif "-" in normalized or oddness >= 2:
        duality = 1
        reasons.append("В имени есть псевдонимный оттенок — это влияет на сюжетные повороты.")

    return NameFeatures(
        formality=clamp(formality),
        oddness=clamp(oddness),
        compactness=clamp(compactness),
        duality=clamp(duality),
        reasons=reasons[:4],
    )
