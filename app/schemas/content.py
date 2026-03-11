from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NameFeatures(BaseModel):
    formality: int
    oddness: int
    compactness: int
    duality: int
    reasons: list[str] = Field(default_factory=list)


class EntityBase(BaseModel):
    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)


class Item(EntityBase):
    utility: int
    status: int
    mobility: int
    tone: str
    tags: list[str] = Field(default_factory=list)
    compatible_blueprints: list[str] = Field(default_factory=list)


class Location(EntityBase):
    publicness: int
    commerce: int
    authority: int
    danger: int
    tags: list[str] = Field(default_factory=list)
    compatible_blueprints: list[str] = Field(default_factory=list)


class Fear(EntityBase):
    social_fear: int
    physical_fear: int
    loss_fear: int
    weird_fear: int
    tags: list[str] = Field(default_factory=list)


class Role(EntityBase):
    compatible_blueprints: list[str]
    tags: list[str] = Field(default_factory=list)


class Threat(EntityBase):
    compatible_blueprints: list[str]
    tags: list[str] = Field(default_factory=list)


class Modifier(EntityBase):
    compatible_blueprints: list[str]
    tags: list[str] = Field(default_factory=list)


class ActionEffect(BaseModel):
    progress_delta: int = 0
    risk_delta: int = 0
    reputation_delta: int = 0
    resource_delta: int = 0


class SceneAction(BaseModel):
    id: str
    label: str
    intent: str
    effects: ActionEffect
    flags_to_add: list[str] = Field(default_factory=list)


class Scene(BaseModel):
    id: str
    blueprint: str
    phase: str
    title: str
    short_text_1: str
    short_text_2: str
    actions: list[SceneAction]


class Blueprint(BaseModel):
    id: str
    name: str
    goal: str


class Ending(BaseModel):
    id: str
    name: str
    title: str
    summary: str
    final_lines: list[str]


class ContentPack(BaseModel):
    items: list[Item]
    locations: list[Location]
    fears: list[Fear]
    roles: list[Role]
    threats: list[Threat]
    modifiers: list[Modifier]
    blueprints: list[Blueprint]
    scenes: list[Scene]
    endings: list[Ending]
    common_names: list[str]
    title_words: list[str]
    aliases: dict[str, dict[str, list[str]]] = Field(default_factory=dict)
    intents: dict[str, list[str]]


class MatchResult(BaseModel):
    entity: EntityBase
    score: float
    adaptation_line: str | None = None
    matched_by: str
    meta: dict[str, Any] = Field(default_factory=dict)
