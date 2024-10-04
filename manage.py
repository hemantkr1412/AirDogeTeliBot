import requests
import time
import asyncio
from telegram import Bot

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

async def get_price_and_send():
    url = "https://airdaomarkets.xyz/api/v1/event/fetch-doge-data/"
    
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(data)
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

                    print(message)
                    
                    # Send message to the Telegram channel
                    await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
                    print("Price update sent.")
                else:
                    print("Price data not available.")
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {e}")

        # Wait for 5 minutes before the next update
        await asyncio.sleep(300)  # 300 seconds = 5 minutes

if __name__ == "__main__":
    # Create an event loop to run the async function
    asyncio.run(get_price_and_send())
