import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta


class ExchangeRatesFetcher:
    def __init__(self):
        self.base_url = "https://api.nbp.pl/api/exchangerates/tables/a/"

    async def fetch_exchange_rates(self, date):
        url = f"{self.base_url}{date}?format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    async def get_exchange_rates_for_last_n_days(self, n):
        today = datetime.today()
        date = (today - timedelta(days=n - 1)).strftime("%Y-%m-%d")
        exchange_rates = []
        data = await self.fetch_exchange_rates(date)
        if data:
            exchange_rates.append({date: self.parse_exchange_rates(data)})
        return exchange_rates

    def parse_exchange_rates(self, data):
        rates = {}
        for currency in data[0]['rates']:
            if currency['code'] in ['USD', 'EUR']:
                rates[currency['code']] = {
                    'sale': currency.get( 'ask', None ),
                    'purchase': currency.get( 'bid', None )
                }
        return rates


async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <number_of_days>")
        return

    try:
        n_days = int(sys.argv[1])
    except ValueError:
        print("Number of days must be an integer")
        return

    if n_days <= 0 or n_days > 10:
        print("Number of days must be between 1 and 10")
        return

    fetcher = ExchangeRatesFetcher()
    exchange_rates = await fetcher.get_exchange_rates_for_last_n_days(n_days)
    print(exchange_rates)


if __name__ == "__main__":
    asyncio.run(main())
