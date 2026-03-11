from app.core.action_parser import parse_action
from app.core.content_loader import load_content
from app.core.ending_engine import choose_ending
from app.core.scene_engine import pick_scene
from app.core.state_engine import apply_action
from app.schemas.game import GameStats


def test_happy_path_four_turns() -> None:
    content = load_content()
    blueprint = "Defense"
    stats = GameStats(progress=4, risk=3, reputation=4, resource=4)
    used = set()
    for turn in range(4):
        scene = pick_scene(content.scenes, blueprint, turn, used)
        used.add(scene.id)
        action = parse_action("проверить", scene.actions, content.intents)
        stats = apply_action(stats, action)
    ending = choose_ending(stats)
    assert ending
    assert stats.progress >= 4
