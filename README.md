Телеграм бот для проекта Taco Squad
=====================
### Канал проекта: https://t.me/tacosquad202420
✨ Возможности
=====================
### Пользовательские

• /start — приветствие, кнопочная клавиатура <br/>• /catalog — показать все товары <br/>• /sale — показать акционные товары <br/>• «Наш канал» — ссылка на канал <br/>• «Задать вопрос» — переслать вопрос администратору
 
### Администраторские
 
• /add_product → диалог добавления товара <br/>• /delete_product — удалить один или несколько товаров <br/>• /add_sale / /delete_sale — то же для акций <br/>• ответ‑реплай на вопрос — переслать ответ пользователю
 
🚀 Быстрый старт
=====================
# 1. клонируем репозиторий
$ git clone https://github.com/your‑org/tacosquad‑bot.git && cd tacosquad‑bot
# 2. создаём и активируем окружение
$ python -m venv .venv <br/>
$ source .venv/bin/activate  # Windows: .venv\Scripts\activate
# 3. ставим зависимости
$ pip install -r requirements.txt
# 4. создаём .env
$ cp .env.example .env <br/>
и вписываем BOT_TOKEN, ADMIN_IDS
# 5. запускаем
$ python main.py
 
### Docker
docker build -t tacosquad-bot . <br/>
docker run -d --env-file .env --name tacosquad tacosquad-bot
 
📂 Структура проекта
=====================
├── admin.py          # FSM и роутеры для администраторов <br/>
├── handlers.py       # пользовательские роутеры <br/>
├── kb.py             # клавиатуры <br/>
├── config.py         # читает .env через python‑dotenv <br/>
├── main.py           # входная точка, диспетчер aiogram <br/>
├── products.json     # товары (создаётся ботом) <br/>
├── sales.json        # акции (создаётся ботом) <br/>
└── requirements.txt  # зависимости <br/>
 
🛠️ Используемые технологии
=====================
{ <br/>
   "language": "Python 3.11", <br/>
   "frameworks": { <br/>
     "aiogram": "3.7.x", <br/>
     "python-dotenv": "1.0.x" <br/>
  }, <br/>
   "runtime": "asyncio", <br/>
   "storage": "JSON files on disk (products.json, sales.json)", <br/>
   "linter_static": "mypy / pylint (optional)", <br/>
   "tools": ["uuid", "re", "logging"] <br/>
} <br/>
