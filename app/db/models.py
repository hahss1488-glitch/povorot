from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    games: Mapped[list[Game]] = relationship(back_populates="user")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(16), default="building")
    blueprint_id: Mapped[str | None] = mapped_column(String(64))
    role_id: Mapped[str | None] = mapped_column(String(64))
    item_id: Mapped[str | None] = mapped_column(String(64))
    location_id: Mapped[str | None] = mapped_column(String(64))
    fear_id: Mapped[str | None] = mapped_column(String(64))
    threat_id: Mapped[str | None] = mapped_column(String(64))
    modifier_id: Mapped[str | None] = mapped_column(String(64))
    original_name_input: Mapped[str | None] = mapped_column(String(255))
    original_item_input: Mapped[str | None] = mapped_column(String(255))
    original_location_input: Mapped[str | None] = mapped_column(String(255))
    original_fear_input: Mapped[str | None] = mapped_column(String(255))
    progress: Mapped[int] = mapped_column(Integer, default=3)
    risk: Mapped[int] = mapped_column(Integer, default=3)
    reputation: Mapped[int] = mapped_column(Integer, default=3)
    resource: Mapped[int] = mapped_column(Integer, default=3)
    turn_number: Mapped[int] = mapped_column(Integer, default=0)
    explanation_lines_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    result_ending_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="games")
    events: Mapped[list[GameEvent]] = relationship(back_populates="game")


class GameEvent(Base):
    __tablename__ = "game_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    turn_number: Mapped[int] = mapped_column(Integer)
    scene_id: Mapped[str] = mapped_column(String(64))
    raw_user_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    chosen_action_id: Mapped[str] = mapped_column(String(64))
    state_before_json: Mapped[dict] = mapped_column(JSON)
    state_after_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    game: Mapped[Game] = relationship(back_populates="events")
