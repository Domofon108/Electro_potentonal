import pandas as pd
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load the data
df = pd.read_csv("Prepared_data.csv")

# Comand /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me the symbol or element number and I will show you the reactions and potentials.")

# Answering to the message
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.isdigit():
        match = df[df['Atomic_Number'] == int(text)]
    else:
        match = df[df['Symbol'].str.lower() == text.lower()]

    if match.empty:
        await update.message.reply_text("Element not found. Try again.")
    else:
        header = f"📋 Reactions for {match.iloc[0]['Symbol']}:\n\n"
        table_lines = ["Reaction".ljust(40) + "| E⁰ (V)",
                       "-" * 40 + "|--------"]
        for _, row in match.iterrows():
            reaction = str(row['Reaction'])[:40].ljust(40)
            potential = str(row['Potential']).rjust(6)
            table_lines.append(f"{reaction}| {potential}")
        
        result = header + "```\n" + "\n".join(table_lines) + "\n```"
        await update.message.reply_text(result, parse_mode='Markdown')

# Основная функция
async def main():
    app = ApplicationBuilder().token("7377149175:AAHkoemPLZVKr77egSpF7Dc1-i32GWBh7uY").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    await app.initialize()
    await app.start()
    print("The bot is running. Press Ctrl+C to stop.")
    await app.updater.start_polling()
    await app.updater.wait_for_stop()
    await app.stop()
    await app.shutdown()

# Launch with protection from "running event loop"
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "asyncio.run()" in str(e) or "event loop is already running" in str(e):
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.create_task(main())
        else:
            raise
