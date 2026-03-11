from app.core.name_analyzer import analyze_name


def test_name_analyzer_features() -> None:
    result = analyze_name("Господин Лис", ["Иван"], ["господин"])
    assert result.formality >= 1
    assert result.duality == 2
    assert result.compactness in {0, 1, 2}
