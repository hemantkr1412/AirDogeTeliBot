import requests
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler

# Your bot token
TELEGRAM_BOT_TOKEN = '7555457560:AAG9kpmrSeIFdvug4aENiafdPKY8yO_0W9M'
# Your channel ID (for public use @username, for private use -100xxxxxxxxx)
TELEGRAM_CHANNEL_ID = '@testing_price_on_py'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Helper function to format numbers
def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"  # Convert to millions
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"  # Convert to thousands
    return str(value)  # If less than 1,000, return as-is

# Function to fetch price data and format the message
async def fetch_price():
    url = "https://airdaomarkets.xyz/api/v1/event/fetch-doge-data/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = data.get('price_in_usdt')
            marketCap = data.get('market_cap')
            current_burn_token = data.get('curr_tokens_burnt')

            # Format market cap and tokens burned
            formatted_marketCap = format_number(marketCap)
            formatted_burn_token = format_number(current_burn_token)

            if price:
                message = f"ADOGE price :${price}.\n" \
                          f"Market Cap: ${formatted_marketCap}.\n" \
                          f"Tokens Burned: {formatted_burn_token}."
                return message
            else:
                return "Price data not available."
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

# Function to handle the /price command
async def price_command(update: Update, context):
    price_message = await fetch_price()
    await update.message.reply_text(price_message)

# Function to handle the /buy command
async def buy_command(update: Update, context):
    buy_message = (
        "Steps on how to buy $ADOGE!\n\n"
        "1. Visit Astra DEX. https://star-fleet.io/astra/swap\n"
        "2. Choose the amount of AMB you wish to use for the purchase.\n"
        "3. Paste the AirDoge contract address: 0x48437113D6d4808bD281F50eEe4b87D4c58D2557 to display the AirDoge token.\n"
        "4. Go to Settings, enable Expert Mode, and set slippage to 7% at least.\n"
        "5. Click Swap to complete the transaction."
    )
    await update.message.reply_text(buy_message)

# Function to handle the /website command
async def website_command(update: Update, context):
    website_message = "airdoge.xyz"
    await update.message.reply_text(website_message)

# Function to send price updates every 5 minutes
async def get_price_and_send():
    while True:
        price_message = await fetch_price()
        if price_message:
            # Send message to the Telegram channel
            await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=price_message)
            print("Price update sent.")
        
        # Wait for 5 minutes before the next update
        await asyncio.sleep(300)  # 300 seconds = 5 minutes

if __name__ == "__main__":
    # Create an Application to handle bot commands
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers for /price, /buy, and /website
    application.add_handler(CommandHandler('price', price_command))
    application.add_handler(CommandHandler('buy', buy_command))
    application.add_handler(CommandHandler('website', website_command))

    # Start fetching price updates and sending them every 5 minutes
    loop = asyncio.get_event_loop()
    loop.create_task(get_price_and_send())

    # Start the bot and listen for commands
    application.run_polling()
