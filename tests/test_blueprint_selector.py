from app.core.blueprint_selector import pick_blueprint
from app.schemas.content import Fear, Item, Location, NameFeatures


def test_blueprint_selector_returns_valid() -> None:
    name = NameFeatures(formality=1, oddness=1, compactness=1, duality=0)
    item = Item(id="i", name="ключ", aliases=[], utility=2, status=1, mobility=2, tone="work")
    location = Location(id="l", name="рынок", aliases=[], publicness=2, commerce=2, authority=1, danger=1)
    fear = Fear(id="f", name="позор", aliases=[], social_fear=2, physical_fear=0, loss_fear=1, weird_fear=0)
    assert pick_blueprint(name, item, location, fear) in {"Defense", "Growth", "Startup", "Recovery"}
