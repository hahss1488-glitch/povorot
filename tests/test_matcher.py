from app.core.matcher import match_entity
from app.schemas.content import Item


def test_matcher_fuzzy() -> None:
    entities = [
        Item(id="1", name="кружка", aliases=["чашка"], utility=1, status=1, mobility=1, tone="household"),
        Item(id="2", name="фонарик", aliases=[], utility=2, status=0, mobility=2, tone="work"),
    ]
    result = match_entity("кружечка", entities)
    assert result.entity.id == "1"
