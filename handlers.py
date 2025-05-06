from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from admin import AddProduct
from admin import load_products 
from admin import load_sales
from aiogram.fsm.context import FSMContext
import config
import kb

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message) -> None:
    await msg.answer(
        "Привет! Это TacoSquad — брендовая одежда с быстрой доставкой.\n"
        "Выбирай действие кнопками или жми /catalog, чтобы посмотреть товары!",
        reply_markup=kb.main_kb,
    )
    await msg.answer(
        "Доставка в течение 5-7 дней по России!\n"
        "Оплата картой или наличными при получении"
    )


@router.message(Command("catalog"))
@router.message(F.text.lower() == "каталог")
async def catalog_handler(msg: Message):
    items = load_products()

    if not items:
        return await msg.answer("Пока нет ни одного товара.")

    admin_id = config.ADMIN_IDS[0]

    for idx, item in enumerate(items, 1):
        caption = f"<b>{item['name']}</b>\nЦена: {item['price']} ₽"

        order_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Заказать",
                        url=f"tg://user?id={admin_id}",
                    )
                ]
            ]
        )

        await msg.answer_photo(
            item["photo"],
            caption=caption,
            reply_markup=order_kb,
        )

@router.message(Command("sale"))
@router.message(F.text.lower() == "акции")
async def sale_handler(msg: Message):
    sales = load_sales()
    if not sales:
        return await msg.answer("Сейчас нет акционных товаров.")

    admin_id = config.ADMIN_IDS[0]

    for it in sales:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Заказать",
                        url=f"tg://user?id={admin_id}",
                    )
                ]
            ]
        )
        caption = f"<b>{it['name']}</b>\nЦена: {it['price']} ₽"
        await msg.answer_photo(it["photo"], caption=caption, reply_markup=kb)


@router.message(F.text.lower() == "наш канал")
async def channel_handler(msg: Message) -> None:
    await msg.answer("🔗 Наш Telegram-канал: \n" \
                    "https://t.me/tacosquad202420")


class AskQuestion(StatesGroup):
    waiting = State()

@router.message(F.text.lower() == "задать вопрос")
async def ask_question(msg: Message, state: FSMContext):
    await msg.answer("Напишите ваш вопрос, и мы ответим как можно скорее:")
    await state.set_state(AskQuestion.waiting)

@router.message(AskQuestion.waiting)
async def receive_question(msg: Message, state: FSMContext):
    await state.clear()

    for admin_id in config.ADMIN_IDS:
        await msg.bot.send_message(
            admin_id,
            (
                f"❓ Вопрос от {msg.from_user.full_name} "
                f"(id: <code>{msg.from_user.id}</code>):\n\n"
                f"{msg.text}\n\n"
                "Ответьте на это сообщение обычным сообщением — оно уйдёт пользователю"
            ),
            parse_mode="HTML",
            )

    await msg.answer("Ваш вопрос отправлен! Мы скоро свяжемся с вами.")