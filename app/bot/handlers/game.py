from __future__ import annotations

import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.common import action_keyboard, build_confirm_keyboard, new_game_keyboard, refreshable_options, start_keyboard
from app.core.action_parser import parse_action
from app.core.blueprint_selector import pick_blueprint
from app.core.build_generator import build_result
from app.core.content_loader import load_content
from app.core.ending_engine import choose_ending
from app.core.matcher import match_entity
from app.core.name_analyzer import analyze_name
from app.core.scene_engine import pick_scene
from app.core.state_engine import apply_action, apply_modifier
from app.core.state_machine import GameFSM
from app.schemas.game import GameStats

router = Router()
content = load_content()


def _sample_names(values: list[str], size: int = 3) -> list[str]:
    return random.sample(values, size)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Добро пожаловать в ПОВОРОТ. Готов к 4-ходовому сюжету?", reply_markup=start_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer("Команды: /start, /newgame, /cancel. Можно выбирать кнопки или писать текстом.")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Процесс остановлен. Набери /newgame, чтобы начать заново.")


@router.message(Command("newgame"))
async def cmd_new_game(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(GameFSM.waiting_for_name)
    await message.answer("Как зовут персонажа?")


@router.callback_query(F.data == "start_game")
async def cb_start_game(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(GameFSM.waiting_for_name)
    await callback.message.answer("Как зовут персонажа?")
    await callback.answer()


@router.message(GameFSM.waiting_for_name)
async def get_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    options = _sample_names([x.name for x in content.items])
    await state.update_data(item_options=options)
    await state.set_state(GameFSM.waiting_for_item)
    await message.answer("Любимый предмет? Можно выбрать кнопку или написать свой.", reply_markup=refreshable_options(options, "item"))


@router.callback_query(GameFSM.waiting_for_item, F.data == "refresh:item")
async def refresh_item(callback: CallbackQuery, state: FSMContext) -> None:
    options = _sample_names([x.name for x in content.items])
    await state.update_data(item_options=options)
    await callback.message.edit_reply_markup(reply_markup=refreshable_options(options, "item"))
    await callback.answer("Варианты обновлены")


@router.callback_query(GameFSM.waiting_for_item, F.data.startswith("item:"))
async def pick_item(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(item=callback.data.split(":", 1)[1])
    await move_to_location(callback.message, state)
    await callback.answer()


@router.message(GameFSM.waiting_for_item)
async def text_item(message: Message, state: FSMContext) -> None:
    await state.update_data(item=message.text)
    await move_to_location(message, state)


async def move_to_location(message: Message, state: FSMContext) -> None:
    options = _sample_names([x.name for x in content.locations])
    await state.update_data(location_options=options)
    await state.set_state(GameFSM.waiting_for_location)
    await message.answer("Где происходит история?", reply_markup=refreshable_options(options, "location"))


@router.callback_query(GameFSM.waiting_for_location, F.data == "refresh:location")
async def refresh_location(callback: CallbackQuery, state: FSMContext) -> None:
    options = _sample_names([x.name for x in content.locations])
    await state.update_data(location_options=options)
    await callback.message.edit_reply_markup(reply_markup=refreshable_options(options, "location"))
    await callback.answer("Варианты обновлены")


@router.callback_query(GameFSM.waiting_for_location, F.data.startswith("location:"))
async def pick_location(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(location=callback.data.split(":", 1)[1])
    await state.set_state(GameFSM.waiting_for_fear)
    await callback.message.answer("Чего ты боишься?")
    await callback.answer()


@router.message(GameFSM.waiting_for_location)
async def text_location(message: Message, state: FSMContext) -> None:
    await state.update_data(location=message.text)
    await state.set_state(GameFSM.waiting_for_fear)
    await message.answer("Чего ты боишься?")


@router.message(GameFSM.waiting_for_fear)
async def get_fear(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    name_features = analyze_name(data["name"], content.common_names, content.title_words)
    item_match = match_entity(data["item"], content.items)
    loc_match = match_entity(data["location"], content.locations)
    fear_match = match_entity(message.text, content.fears)
    blueprint = pick_blueprint(name_features, item_match.entity, loc_match.entity, fear_match.entity)
    adaptations = [x for x in [item_match.adaptation_line, loc_match.adaptation_line, fear_match.adaptation_line] if x]
    build = build_result(content, blueprint, name_features, item_match.entity, loc_match.entity, fear_match.entity, adaptations)
    await state.update_data(
        fear=message.text,
        name_features=name_features.model_dump(),
        item_id=item_match.entity.id,
        location_id=loc_match.entity.id,
        fear_id=fear_match.entity.id,
        build=build.model_dump(),
        stats=build.stats.model_dump(),
        turn_number=0,
        used_scenes=[],
    )

    role = next(x.name for x in content.roles if x.id == build.role_id)
    threat = next(x.name for x in content.threats if x.id == build.threat_id)
    modifier = next(x.name for x in content.modifiers if x.id == build.modifier_id)
    card = (
        f"Кто ты: {role}\nТип сюжета: {build.blueprint_id}\nУгроза: {threat}\nОсобенность: {modifier}\n"
        f"Цель: {build.goal}\n\nПочему так вышло:\n- " + "\n- ".join(build.explanation_lines)
    )
    await state.set_state(GameFSM.waiting_for_build_confirm)
    await message.answer(card, reply_markup=build_confirm_keyboard())


@router.callback_query(GameFSM.waiting_for_build_confirm, F.data == "rebuild")
async def rebuild(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    fear_text = data.get("fear", "страх")
    msg = callback.message
    if msg is None:
        await callback.answer("Не удалось пересобрать", show_alert=True)
        return
    msg.text = fear_text
    await get_fear(msg, state)
    await callback.answer("Пересобрано")


@router.callback_query(GameFSM.waiting_for_build_confirm, F.data == "confirm_build")
async def confirm_build(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(GameFSM.waiting_for_turn_action)
    await send_turn(callback.message, state)
    await callback.answer()


async def send_turn(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    turn = data.get("turn_number", 0)
    build = data["build"]
    if turn >= 4:
        stats = GameStats(**data["stats"])
        ending_id = choose_ending(stats)
        ending = next(e for e in content.endings if e.id == ending_id)
        text = f"{ending.title}\n{ending.summary}\n" + "\n".join(ending.final_lines)
        await state.clear()
        await message.answer(text, reply_markup=new_game_keyboard())
        return

    used = set(data.get("used_scenes", []))
    scene = pick_scene(content.scenes, build["blueprint_id"], turn, used)
    used.add(scene.id)
    stats = GameStats(**data["stats"])
    stat_line = f"Прогресс: {stats.progress}/10 | Риск: {stats.risk}/10 | Репутация: {stats.reputation}/10 | Ресурс: {stats.resource}/10"
    await state.update_data(current_scene=scene.model_dump(), used_scenes=list(used))
    actions = [(a.id, a.label) for a in scene.actions]
    await message.answer(f"Ход {turn+1}/4 — {scene.title}\n{scene.short_text_1}\n{scene.short_text_2}\n\n{stat_line}", reply_markup=action_keyboard(actions))


@router.callback_query(GameFSM.waiting_for_turn_action, F.data.startswith("act:"))
async def action_click(callback: CallbackQuery, state: FSMContext) -> None:
    aid = callback.data.split(":", 1)[1]
    data = await state.get_data()
    scene_actions = data["current_scene"]["actions"]
    chosen = next(a for a in scene_actions if a["id"] == aid)
    await process_turn(callback.message, state, chosen, None)
    await callback.answer()


@router.message(GameFSM.waiting_for_turn_action)
async def action_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    from app.schemas.content import SceneAction

    actions = [SceneAction.model_validate(a) for a in data["current_scene"]["actions"]]
    chosen = parse_action(message.text, actions, content.intents)
    await process_turn(message, state, chosen.model_dump(), message.text)


async def process_turn(message: Message, state: FSMContext, chosen_action: dict, raw_text: str | None) -> None:
    from app.schemas.content import Modifier, SceneAction

    data = await state.get_data()
    build = data["build"]
    stats_before = GameStats(**data["stats"])
    action = SceneAction.model_validate(chosen_action)
    stats_after = apply_action(stats_before, action)
    modifier = Modifier.model_validate(next(m for m in content.modifiers if m.id == build["modifier_id"]).model_dump())
    stats_after = apply_modifier(modifier, stats_before, stats_after, action)
    await state.update_data(stats=stats_after.model_dump(), turn_number=data.get("turn_number", 0) + 1)
    await message.answer(f"Принято: {action.label}")
    await send_turn(message, state)
