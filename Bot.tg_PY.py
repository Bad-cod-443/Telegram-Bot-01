import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

TOKEN = "7861543830:AAHlfqR67qHj_XfziWIzeJHYWXalrvns9xY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним баланс в памяти (словарь {user_id: balance})
user_balances = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    user_balances[message.from_user.id] = 0.0
    await message.reply("👋 Привет! Чем могу помочь?\n\n"
                        "Используй команды:\n"
                        "➕ Доход: + сумма описание\n"
                        "➖ Расход: - сумма описание\n"
                        "💰 Баланс: /balance\n")

@dp.message(Command("balance"))
async def balance(message: types.Message):
    balance = user_balances.get(message.from_user.id, 0.0)
    await message.reply(f"💰 Твой текущий баланс: {balance:.2f} руб.")

@dp.message()
async def handle_finances(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    try:
        sign, rest = text[0], text[1:].strip()
        amount_str, *_ = rest.split(maxsplit=1)
        amount = float(amount_str.replace(',', '.'))

        if sign == '+':
            user_balances[user_id] += amount
            await message.reply(f"✅ Доход {amount:.2f} руб. добавлен.\n"
                                f"Текущий баланс: {user_balances[user_id]:.2f} руб.")
        elif sign == '-':
            user_balances[user_id] -= amount
            await message.reply(f"✅ Расход {amount:.2f} руб. учтён.\n"
                                f"Текущий баланс: {user_balances[user_id]:.2f} руб.")
        else:
            await message.reply("🤔 Я не понял команду. Используй + или - перед суммой.")
    except (ValueError, IndexError):
        await message.reply("❌ Неверный формат команды.\n"
                            "Используй формат:\n"
                            "+ 100 зарплата\n"
                            "- 50 продукты")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())