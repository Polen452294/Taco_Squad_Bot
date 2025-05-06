import json
import re
import os
import uuid
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.filters.command import CommandObject
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command 
from aiogram.enums import ParseMode 

import config

router = Router()

USER_ID_RE = re.compile(r"id:\s*(\d+)", re.I) 

PRODUCTS_FILE = "products.json"


def load_products() -> list[dict]:
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_products(items: list[dict]) -> None:
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


class AddProduct(StatesGroup):
    name = State()
    price = State()
    photo = State()


@router.message(Command("add_product")) 
async def cmd_add_product(msg: Message, state: FSMContext):
    if msg.from_user.id not in config.ADMIN_IDS:
        return await msg.answer("⛔ Команда доступна только администратору")
    await msg.answer("Введите название товара:")
    await state.set_state(AddProduct.name)


@router.message(AddProduct.name)
async def st_name(msg: Message, state: FSMContext) -> None:
    await state.update_data(name=msg.text.strip())
    await msg.answer("Введите цену в рублях:")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
async def st_price(msg: Message, state: FSMContext) -> None:
    if not msg.text.isdigit():
        return await msg.answer("Цена должна быть числом. Попробуйте ещё раз:")
    await state.update_data(price=int(msg.text))
    await msg.answer("Отправьте фото товара:")
    await state.set_state(AddProduct.photo)


@router.message(AddProduct.photo, F.photo)
async def st_photo(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photo_id = msg.photo[-1].file_id

    items = load_products()
    items.append(
        {"name": data["name"], "price": data["price"], "photo": photo_id}
    )
    save_products(items)

    await msg.answer("✅ Товар добавлен!")
    await state.clear()

@router.message(Command("delete_product"))
async def cmd_delete_product(msg: Message):
    if msg.from_user.id not in config.ADMIN_IDS:
        return await msg.answer("⛔ Команда доступна только администратору.")

    items = load_products()

    changed = False
    for it in items:
        if "id" not in it:
            it["id"] = str(uuid.uuid4())
            changed = True
    if changed:
        save_products(items)

    if not items:
        return await msg.answer("Сейчас в каталоге нет товаров.")

    for item in items:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🗑 Удалить",
                        callback_data=f"del_{item['id']}", 
                    )
                ]
            ]
        )
        caption = f"<b>{item['name']}</b>\nЦена: {item['price']} ₽"
        await msg.answer_photo(item["photo"], caption=caption, reply_markup=kb)

@router.callback_query(F.data.startswith("del_"))
async def cb_delete_product(call: CallbackQuery):
    if call.from_user.id not in config.ADMIN_IDS:
        return await call.answer("Недостаточно прав.", show_alert=True)

    prod_id = call.data[4:]
    items = load_products()

    for i, it in enumerate(items):
        if it.get("id") == prod_id:
            deleted = items.pop(i)
            save_products(items)

            await call.message.edit_caption(
                caption=f"❌ <s>{deleted['name']} (удалено)</s>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[]),
            )

            await call.answer("Товар удалён", show_alert=True)
            return

    await call.answer("Этот товар уже удалён.", show_alert=True)

@router.message(AddProduct.photo, F.photo)
async def st_photo(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photo_id = msg.photo[-1].file_id

    items = load_products()
    items.append(
        {
            "id": str(uuid.uuid4()), 
            "name": data["name"],
            "price": data["price"],
            "photo": photo_id,
        }
    )
    save_products(items)
    await msg.answer("✅ Товар добавлен!")
    await state.clear()

SALES_FILE = "sales.json"


def load_sales() -> list[dict]:
    if not os.path.exists(SALES_FILE):
        return []
    with open(SALES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sales(items: list[dict]) -> None:
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

class AddSale(StatesGroup):
    name = State()
    price = State()
    photo = State()

@router.message(Command("add_sale"))
async def cmd_add_sale(msg: Message, state: FSMContext):
    if msg.from_user.id not in config.ADMIN_IDS:
        return await msg.answer("⛔ Команда доступна только администратору.")
    await msg.answer("Введите название акционного товара:")
    await state.set_state(AddSale.name)


@router.message(AddSale.name)
async def sale_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip())
    await msg.answer("Введите акционную цену:")
    await state.set_state(AddSale.price)


@router.message(AddSale.price)
async def sale_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("Цена должна быть числом. Попробуйте ещё раз:")
    await state.update_data(price=int(msg.text))
    await msg.answer("Отправьте фото акционного товара:")
    await state.set_state(AddSale.photo)


@router.message(AddSale.photo, F.photo)
async def sale_photo(msg: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = msg.photo[-1].file_id
    items = load_sales()
    items.append(
        {
            "id": str(uuid.uuid4()),
            "name": data["name"],
            "price": data["price"],
            "photo": photo_id,
        }
    )
    save_sales(items)
    await msg.answer("✅ Акционный товар добавлен!")
    await state.clear()

@router.message(Command("delete_sale"))
async def cmd_delete_sale(msg: Message):
    if msg.from_user.id not in config.ADMIN_IDS:
        return await msg.answer("⛔ Команда доступна только администратору.")

    items = load_sales()
    if not items:
        return await msg.answer("Список акционных товаров пуст.")

    # показываем все акции
    for it in items:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🗑 Удалить",
                        callback_data=f"sdel_{it['id']}",
                    )
                ]
            ]
        )
        caption = f"<b>{it['name']}</b>\nЦена: {it['price']} ₽"
        await msg.answer_photo(it["photo"], caption=caption, reply_markup=kb)

@router.callback_query(F.data.startswith("sdel_"))
async def cb_delete_sale(call: CallbackQuery):
    if call.from_user.id not in config.ADMIN_IDS:
        return await call.answer("Недостаточно прав.", show_alert=True)

    sale_id = call.data[5:]    
    sales = load_sales()

    for i, item in enumerate(sales):
        if item["id"] == sale_id:
            deleted = sales.pop(i)
            save_sales(sales)

            await call.message.edit_caption(
                caption=f"❌ <s>{deleted['name']} (удалено)</s>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[]),
            )

            await call.answer("Акция удалена", show_alert=True)
            return

    await call.answer("Уже удалено.", show_alert=True)

@router.message(Command("reply"))
async def cmd_reply(msg: Message, command: CommandObject):
    if msg.from_user.id not in config.ADMIN_IDS:
        return await msg.answer("⛔ Только администратор может использовать /reply.")

    if not command.args:
        return await msg.answer("Формат: /reply <user_id> <текст ответа>")

    parts = command.args.split(maxsplit=1)
    if len(parts) < 2 or not parts[0].isdigit():
        return await msg.answer("Формат: /reply <user_id> <текст ответа>")

    user_id, answer_text = int(parts[0]), parts[1]

    try:
        await msg.bot.send_message(
            user_id,
            f"💬 Ответ от TacoSquad:\n\n{answer_text}",
        )
        await msg.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await msg.answer(f"❌ Не удалось отправить сообщение:\n{e}")

@router.message(
    F.reply_to_message,   
    F.from_user.id.in_(config.ADMIN_IDS) 
)
async def relay_answer(msg: Message):
    original = msg.reply_to_message

    if not original or not original.text:
        return                      

    match = USER_ID_RE.search(original.text)
    if not match:
        return

    user_id = int(match.group(1))

    try:
        await msg.bot.send_message(
            user_id,
            f"💬 Ответ от TacoSquad:\n\n{msg.text}",
        )
        await msg.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await msg.answer(f"❌ Не удалось доставить сообщение:\n{e}")