from pydantic import BaseModel


class GameStats(BaseModel):
    progress: int
    risk: int
    reputation: int
    resource: int


class BuildResult(BaseModel):
    blueprint_id: str
    role_id: str
    threat_id: str
    modifier_id: str
    goal: str
    explanation_lines: list[str]
    stats: GameStats
