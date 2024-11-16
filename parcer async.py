import asyncio
import aiohttp
import json
import time

url = "https://www.okx.com/api/v5/market/books"
coins = ["BTC-USDT", "ETH-USDT", "BNB-USDT"]

async def get_order_book(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}?instId={symbol}") as response:
            if response.status == 200:
                data = await response.json()
                order_book = {
                    symbol: {
                        "asks": data['data'][0]['asks'],
                        "bids": data['data'][0]['bids']
                    }
                }
                return order_book
            else:
                print(f"Ошибка при получении ордербука {symbol}: {response.status}")
                return None

async def fetch_all_order_books():
    tasks = [get_order_book(symbol) for symbol in coins]
    results = await asyncio.gather(*tasks)
    return results

def save_to_json(data, filename="order_books.json"):
    with open(filename, "w", encoding="UTF-8") as res:
        json.dump(data, res, indent=4)

async def main():
    start_time = time.time()
    order_books = await fetch_all_order_books()
    order_books = [book for book in order_books if book is not None]
    save_to_json(order_books)
    end_time = time.time()
    print(f"Время выполнения программы: {end_time - start_time:.2f} секунд")

asyncio.run(main())