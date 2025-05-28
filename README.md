# ⚡ ElectroPotentialBot 🤖  
> Discover standard electrode potentials and redox reactions — instantly, via Telegram.

---

## 🌟 About the Project

**ElectroPotentialBot** is a Telegram bot that provides quick access to electrochemical redox reactions and their standard electrode potentials (E⁰) based on either the **element symbol** or **atomic number**.

Whether you're a student, researcher, or chemistry enthusiast — this bot is a handy reference for electrochemistry at your fingertips.

---

## 📦 Features

- 🔍 Search by **chemical symbol** (e.g. `Zn`) or **atomic number** (e.g. `30`)
- 🧪 Shows **reduction half-reactions** with associated **standard electrode potentials**
- 📊 Formats results as clean, readable Markdown tables
- 🔁 Powered by **pandas** for fast lookups
- 🌐 Easy deployment on cloud or local environments

---

## 🚀 Usage

1. Start the bot with `/start`
2. Send a chemical symbol or atomic number
3. Instantly receive relevant redox reactions and E⁰ values!

**Example:**

Input: Zn
Output:
📋 Reactions for Zn:
──────────────────────────────────────────── | E⁰ (V)
Zn²⁺ + 2e⁻ ⇌ Zn | -0.76


---

## 🛠️ Tech Stack

- Python 3.9+
- [python-telegram-bot v20+](https://github.com/python-telegram-bot/python-telegram-bot)
- pandas
- asyncio
- dotenv

---

## 📁 Project Structure

├── bot.py # Telegram bot logic
├── Prepared_data.csv # Redox reactions and potentials
├── .env # Contains your TELEGRAM_BOT_TOKEN
└── README.md # Project documentation

## 🧠 Data Source

The Prepared_data.csv file contains a curated list of standard redox reactions and their electrode potentials, compiled from reputable electrochemical databases and textbooks.
## 🤝 Contributing

Pull requests, suggestions, and issue reports are welcome!
Let’s make electrochemistry more accessible — together.
