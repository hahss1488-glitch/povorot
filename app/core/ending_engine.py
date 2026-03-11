from app.schemas.game import GameStats


def choose_ending(stats: GameStats) -> str:
    p, r, rep, res = stats.progress, stats.risk, stats.reputation, stats.resource
    if p >= 8 and r <= 4 and rep >= 6:
        return "clean_victory"
    if p >= 8 and r <= 7 and rep <= 5:
        return "dirty_victory"
    if p >= 7 and rep <= 3:
        return "shameful_triumph"
    if p >= 6 and r <= 4 and res >= 4:
        return "quiet_success"
    if p >= 8 and res <= 1:
        return "pyrrhic_victory"
    if p >= 7 and rep >= 8:
        return "success_on_trust"
    if p >= 7 and res >= 7:
        return "success_on_resource"
    if p <= 5 and rep >= 6 and r >= 6:
        return "honorable_failure"
    if p <= 4 and r >= 8 and rep <= 4:
        return "comic_failure"
    if p <= 3 and r >= 9:
        return "collapse_under_pressure"
    if p in [5, 6] and r in [5, 6]:
        return "draw"
    return "beautiful_disaster"
