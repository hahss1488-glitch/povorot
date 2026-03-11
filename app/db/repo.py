from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Game, GameEvent, User


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: str | None, first_name: str | None) -> User:
        query = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        user = query.scalar_one_or_none()
        if user:
            user.username = username
            user.first_name = first_name
            await self.session.commit()
            return user
        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_game(self, user_id: int) -> Game:
        game = Game(user_id=user_id, status="building")
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def get_latest_game(self, user_id: int) -> Game | None:
        query = await self.session.execute(select(Game).where(Game.user_id == user_id).order_by(Game.id.desc()))
        return query.scalars().first()

    async def save_event(
        self,
        game_id: int,
        turn_number: int,
        scene_id: str,
        raw_user_input: str | None,
        chosen_action_id: str,
        before: dict,
        after: dict,
    ) -> None:
        event = GameEvent(
            game_id=game_id,
            turn_number=turn_number,
            scene_id=scene_id,
            raw_user_input=raw_user_input,
            chosen_action_id=chosen_action_id,
            state_before_json=before,
            state_after_json=after,
        )
        self.session.add(event)
        await self.session.commit()

    async def finish_game(self, game: Game, ending_id: str) -> None:
        game.status = "finished"
        game.result_ending_id = ending_id
        game.ended_at = datetime.now(tz=timezone.utc)
        await self.session.commit()
