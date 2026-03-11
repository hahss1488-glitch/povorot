from __future__ import annotations

import random

from app.schemas.content import Fear, Item, Location, NameFeatures


def pick_blueprint(name: NameFeatures, item: Item, location: Location, fear: Fear) -> str:
    scores = {
        "Defense": location.danger + item.utility + fear.loss_fear + name.compactness + random.random(),
        "Growth": location.commerce + item.utility + item.mobility + name.oddness + random.random(),
        "Startup": location.publicness
        + location.authority
        + item.status
        + fear.social_fear
        + name.formality
        + random.random(),
        "Recovery": location.danger
        + fear.physical_fear
        + fear.weird_fear
        + name.duality
        + name.oddness
        + random.random(),
    }
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(ordered) > 1 and abs(ordered[0][1] - ordered[1][1]) < 0.3:
        return random.choice([ordered[0][0], ordered[1][0]])
    return ordered[0][0]
