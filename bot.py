import pandas as pd
import asyncio
import nest_asyncio
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables (safe token storage)
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Check token presence
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables.")

# Load data safely
try:
    df = pd.read_csv("Prepared_data.csv")
except FileNotFoundError:
    logger.error("Prepared_data.csv not found.")
    df = pd.DataFrame()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me the symbol or atomic number and I’ll show you redox reactions and potentials.")

# Main response logic
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if df.empty:
        await update.message.reply_text("⚠️ Data not loaded. Please try again later.")
        return

    match = None
    try:
        if text.isdigit():
            match = df[df['Atomic_Number'] == int(text)]
        else:
            match = df[df['Symbol'].str.lower() == text.lower()]
    except Exception as e:
        logger.exception("Error during matching:")
        await update.message.reply_text("❌ Unexpected error occurred while processing your request.")
        return

    if match is None or match.empty:
        await update.message.reply_text("Element not found. Please try again.")
    else:
        header = f"📋 Reactions for {match.iloc[0]['Symbol']}:\n\n"
        table_lines = ["Reaction".ljust(40) + "| E⁰ (V)",
                       "-" * 40 + "|--------"]
        for _, row in match.iterrows():
            reaction = str(row.get('Reaction', 'N/A'))[:40].ljust(40)
            potential = str(row.get('Potential', 'N/A')).rjust(6)
            table_lines.append(f"{reaction}| {potential}")

        result = header + "```\n" + "\n".join(table_lines) + "\n```"

        # Try Markdown format safely
        try:
            await update.message.reply_text(result, parse_mode='Markdown')
        except Exception as e:
            logger.warning("Markdown parsing failed, sending as plain text.")
            await update.message.reply_text(result)

# Main bot launch function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    logger.info("Bot is running.")
    await app.run_polling()


# Run safely
if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()


